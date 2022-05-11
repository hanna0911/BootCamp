from .api_util import *
from .models import *


def create_notification(request: HttpRequest):
    """
    POST
    {
        'action': 'create notification',
        'title': __TITLE__,
        'content': __CONTENT__(只是公告内容，不是ContentTable那种Content！！)
        'assignees': ['USERNAME1', 'USERNAME2', ... ]
    }
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    action = data.get('action')
    title = data.get('title')
    content = data.get('content')
    assignee_usernames = data.get('assignees')
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if action != 'create notification' or title is None or content is None or assignee_usernames is None:
        return gen_standard_response(400, {'result': 'failure', 'message': 'Bad Arguments'})
    if username is None or role is None:
        return session_timeout_response()
    if role != 'admin' and role != 'HRBP' and role != 'teacher':
        return unauthorized_action_response()
    assignees = []
    for assignee_username in assignee_usernames:
        assignee = PrivateInfo.objects.filter(username=assignee_username).first()
        if assignee is None:
            return item_not_found_error_response()
        assignees.append(assignee)
    author = PrivateInfo.objects.filter(username=username).first()
    if author is None:
        return item_not_found_error_response()
    new_notification = NotificationTable(title=title, content=content, author_name=author.name, author_role=role)
    new_notification.save()
    for assignee in assignees:
        new_user_notification_relation = UserNotificationTable(user=assignee, notification=new_notification)
        new_user_notification_relation.save()
    return gen_standard_response(200, {
        'result': 'success',
        'message': f'notification {title} assigned to {len(assignees)} users'
    })


def my_notifications(request: HttpRequest):
    """
    GET all notifications
    """
    if request.method != 'GET':
        return illegal_request_type_error_response()
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if username is None or role is None:
        return session_timeout_response()
    user = PrivateInfo.objects.filter(username=username).first()
    if user is None:
        return unauthorized_action_response()
    # release scheduled notifications as decoy notifications
    scheduled_relations = UserScheduledTable.objects.filter(user__username=username)
    for scheduled_relation in scheduled_relations:
        scheduled_notification = scheduled_relation.scheduled_notification
        if scheduled_notification.scheduledReleaseTime <= cn_datetime_now():
            decoy_notification = NotificationTable(
                author_name='通知系统',
                author_role='Bootcamp',
                title=scheduled_notification.title,
                content=scheduled_notification.content,
                releaseTime=scheduled_notification.scheduledReleaseTime
            )
            decoy_notification.save()
            user_decoy_relation = UserNotificationTable(
                user=user,
                notification=decoy_notification,
            )
            user_decoy_relation.save()

    notification_list = []
    # 扫描一般公告
    relations = UserNotificationTable.objects.filter(user__username=username)
    for relation in relations:
        notification = relation.notification
        notification_list.append({
            'title': notification.title,
            'content': notification.content,
            'author': notification.author_name,
            'authorRole': notification.author_role,
            'releaseTime': notification.releaseTime,
            'notificationID': notification.id,
            'finished': relation.finished
        })
    # 扫描定时公告
    '''
    scheduledRelations = UserScheduledTable.objects.filter(user__username=username)
    for scheduledRelation in scheduledRelations:
        notification = scheduledRelation.scheduled_notification
        if notification.scheduledReleaseTime <= cn_datetime_now():
            notification_list.append({
            'title': notification.title,
            'content': notification.content,
            'author': '系统生成',
            'authorRole': '系统',
            'releaseTime': notification.scheduledReleaseTime,
            'notificationID': notification.id,
            #'finished': relation.finished
            })
    '''

    return gen_standard_response(200, {
        'result': 'success',
        'message': 'notification list retrieved',
        'notifications': notification_list
    })


def finish_notification(request: HttpRequest):
    """
    POST
    {
        'action': 'finish notification',
        'notificationID': __NOTIFICATION_ID__,
    }
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    action = data.get('action')
    notification_id = data.get('notificationID')
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if action != 'finish notification' or notification_id is None:
        return gen_standard_response(400, {'result': 'failed', 'message': 'Bad Arguments'})
    if username is None or role is None:
        return session_timeout_response()
    relation = UserNotificationTable.objects.filter(user__username=username,
                                                    notification__id=notification_id).first()
    if relation is None:
        return item_not_found_error_response()
    if relation.finished is True:
        return gen_standard_response(200, {'result': 'failed', 'message': 'already finished!'})
    relation.save()
    return gen_standard_response(200, {
        'result': 'success',
        'message': f'finished reading notification {notification_id}'})


def create_group(request: HttpRequest):
    """
    POST
    {
        'action': 'create group',
        'groupName': __GROUP_NAME__,
        'members': [USERNAME1, USERNAME2, ... ]
    }
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    action = data.get('action')
    member_usernames = data.get('members')
    group_name = data.get('groupName')
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if action != 'create group' or member_usernames is None or group_name is None:
        return gen_standard_response(400, {'result': 'failed', 'message': 'Bad Arguments'})
    if username is None or role is None:
        return session_timeout_response()
    if role != 'admin' and role != 'HRBP' and role != 'teacher':
        return unauthorized_action_response()
    user = PrivateInfo.objects.filter(username=username).first()
    if user is None:
        return item_not_found_error_response()
    members = []
    for member_username in member_usernames:
        member = PrivateInfo.objects.filter(username=member_username).first()
        if member is None:
            return item_not_found_error_response()
        members.append(member)
    new_group = GroupTable(creator=user, name=group_name)
    new_group.save()
    for member in members:
        new_relation = UserGroupTable(user=member, group=new_group)
        new_relation.save()
        new_group.user_count += 1
        new_group.save()
    return gen_standard_response(200, {
        'result': 'success',
        'message': f'created new group with id {new_group.id}, which now has {new_group.user_count} users'
    })


def add_group_member(request: HttpRequest):
    """
    POST
    {
        'action': 'add group member'
        'groupID': __GROUP_ID__,
        'username': [USERNAME1, USERNAME2, ... ]
    }
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    action = data.get('action')
    group_id = data.get('groupID')
    target_usernames = data.get('username')
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if action != 'add group member' or group_id is None or target_usernames is None:
        return gen_standard_response(400, {'result': 'failed', 'message': 'Bad Arguments'})
    if username is None or role is None:
        return session_timeout_response()
    if role != 'admin' and role != 'HRBP' and role != 'teacher':
        return unauthorized_action_response()
    # try:
    #     group_id = eval(group_id)
    # except Exception as e:
    #     print(e)
    #     return gen_standard_response(400, {'result': 'failed', 'message': 'Bad Arguments'})
    group = GroupTable.objects.filter(id=group_id).first()
    for target_username in target_usernames:
        target_user = PrivateInfo.objects.filter(username=target_username).first()
        user = PrivateInfo.objects.filter(username=username).first()
        if group is None or target_user is None or user is None:
            return item_not_found_error_response()
        if group.creator.username != username:
            return unauthorized_action_response()
        new_relation = UserGroupTable(user=target_user, group=group)
        new_relation.save()
    return gen_standard_response(200, {
        'result': 'success',
        'message': f'users {target_usernames} added to group {group.name}'
    })


def my_group_list(request: HttpRequest):
    """
    GET
    """
    if request.method != 'GET':
        return illegal_request_type_error_response()
    username = request.session.get('username')
    role = request.session.get('role')
    if username is None or role is None:
        return session_timeout_response()
    user = PrivateInfo.objects.filter(username=username)
    if user is None:
        return unknown_error_response()
    my_groups = GroupTable.objects.filter(creator__username=username)
    group_list = []
    for group in my_groups:
        member_list = []
        member_group_relations = UserGroupTable.objects.filter(group__id=group.id)
        for relation in member_group_relations:
            member_list.append({
                'username': relation.user.username,
                'name': relation.user.name,
                'dept': relation.user.dept
            })
        group_list.append({
            'groupID': group.id,
            'groupName': group.name,
            'members': member_list
        })
    return gen_standard_response(200, {
        'result': 'success',
        'message': f'a total of {len(group_list)} groups retrieved',
        'groups': group_list
    })


def create_group_notification(request: HttpRequest):
    """
    POST
    {
        'action': 'create group notification',
        'title': __TITLE__,
        'content': __CONTENT__(只是公告内容，不是ContentTable那种Content！！)
        'groups': ['GROUP1', 'GROUP2', ... ]
    }
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    action = data.get('action')
    title = data.get('title')
    content = data.get('content')
    group_ids = data.get('groups')
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if action != 'create group notification' or title is None or content is None or group_ids is None:
        return gen_standard_response(400, {'result': 'failure', 'message': 'Bad Arguments'})
    if username is None or role is None:
        return session_timeout_response()
    if role != 'admin' and role != 'HRBP' and role != 'teacher':
        return unauthorized_action_response()
    author = PrivateInfo.objects.filter(username=username).first()
    if author is None:
        return item_not_found_error_response()
    new_notification = NotificationTable(title=title, content=content, author_name=author.name, author_role=role)
    new_notification.save()
    for group_id in group_ids:
        user_group_relations = UserGroupTable.objects.filter(group__id=group_id)
        assignees = []
        if len(user_group_relations) == 0:
            return item_not_found_error_response()
        for user_group_relation in user_group_relations:
            assignee = user_group_relation.user
            assignees.append(assignee)
        for assignee in assignees:
            if UserNotificationTable.objects.filter(user=assignee, notification=new_notification).first() is None:
                new_user_notification_relation = UserNotificationTable(user=assignee, notification=new_notification)
                new_user_notification_relation.save()
    return gen_standard_response(200, {
        'result': 'success',
        'message': f'notification {title} assigned to {len(group_ids)} groups'
    })


def delete_group(request: HttpRequest):
    """
    POST
    action: 'delete group'
    groupID: __GROUP_ID__
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    action = data.get('action')
    group_id = data.get('groupID')
    username = request.session.get('username')
    role = request.session.get('role')
    if action != 'delete group' or group_id is None:
        return gen_standard_response(400, {'result': 'failure', 'message': 'Bad Arguments'})
    if username is None or role is None:
        return session_timeout_response()
    if role != 'admin' and role != 'HRBP' and role != 'teacher':
        return unauthorized_action_response()
    user = PrivateInfo.objects.filter(username=username).first()
    group = GroupTable.objects.filter(id=group_id).first()
    group_name = group.name
    if user is None or group is None:
        return item_not_found_error_response()
    if user != group.creator:
        return unauthorized_action_response()
    user_group_relations = UserGroupTable.objects.filter(group=group)
    length = len(user_group_relations)
    user_group_relations.delete()
    group.delete()
    return gen_standard_response(200, {
        'result': 'success',
        'message': f'group {group_name} with {length} users deleted'
    })


def delete_member(request: HttpRequest):
    """
    POST
    action: 'delete member',
    groupID: __GROUP_ID__,
    memberUsername: __USERNAME__,
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    action = data.get('action')
    group_id = data.get('groupID')
    member_username = data.get('memberUsername')
    username = request.session.get('username')
    role = request.session.get('role')
    if action != 'delete member' or group_id is None or member_username is None:
        return gen_standard_response(400, {'result': 'failure', 'message': 'Bad Arguments'})
    if username is None or role is None:
        return session_timeout_response()
    if role != 'admin' and role != 'HRBP' and role != 'teacher':
        return unauthorized_action_response()
    target_user = PrivateInfo.objects.filter(username=member_username).first()
    user = PrivateInfo.objects.filter(username=username).first()
    group = GroupTable.objects.filter(id=group_id).first()
    target_relation = UserGroupTable.objects.filter(user=target_user, group=group).first()
    if user is None or group is None or target_user is None or target_relation is None:
        return item_not_found_error_response()
    if user != group.creator:
        return unauthorized_action_response()
    target_relation.delete()
    return gen_standard_response(200, {
        'result': 'success',
        'message': f'user {target_user.name} removed from group {group.name}'
    })


def delete_notification(request: HttpRequest):
    """
    POST
    action: 'delete notification',
    notificationID: __NOTIFICATION_ID__
    """
    if request.method != 'POST':
        return illegal_request_type_error_response()
    try:
        data = json.loads(request.body)
    except Exception as e:
        print(e)
        return unknown_error_response()
    action = data.get('action')
    notification_id = data.get('notificationID')
    username = request.session.get('username')
    role = request.session.get('role')
    if action != 'delete notification' or notification_id is None:
        return gen_standard_response(400, {'result': 'failure', 'message': 'Bad Arguments'})
    if username is None or role is None:
        return session_timeout_response()
    user = PrivateInfo.objects.filter(username=username).first()
    if user is None:
        return item_not_found_error_response()
    notification = NotificationTable.objects.filter(id=notification_id).first()
    if notification is None:
        return item_not_found_error_response()
    relations = UserNotificationTable.objects.filter(notification=notification)
    relations.delete()
    notification.delete()
    return gen_standard_response(200, {
        'result': 'success',
        'message': 'notification deleted'
    })


def authored_notification_list(request: HttpRequest):
    if request.method != 'GET':
        return illegal_request_type_error_response()
    session = request.session
    username = session.get('username')
    role = session.get('role')
    if username is None or role is None:
        return session_timeout_response()
    user = PrivateInfo.objects.filter(username=username).first()
    if user is None:
        return unauthorized_action_response()
    notification_list = []
    # 扫描一般公告
    notifications = NotificationTable.objects.filter(author_name=user.name)
    for notification in notifications:
        notification_list.append({
            'title': notification.title,
            'content': notification.content,
            'author': notification.author_name,
            'authorRole': notification.author_role,
            'releaseTime': notification.releaseTime,
            'notificationID': notification.id,
        })
    return gen_standard_response(200, {
        'result': 'success',
        'message': 'authored notification list retrieved',
        'notifications': notification_list
    })
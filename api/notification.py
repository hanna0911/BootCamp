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
    relations = UserNotificationTable.objects.filter(user__username=username)
    notification_list = []
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
    relation.finished = True
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

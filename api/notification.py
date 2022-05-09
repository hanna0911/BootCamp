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
    new_notification = NotificationTable(title=title, content=content, author=author, author_role=role)
    new_notification.save()
    for assignee in assignees:
        new_user_notification_relation = UserNotificationTable(user=assignee, notification=new_notification,)
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
            'author': notification.author.username,
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

''' status serializers '''
from uuid import uuid4


def get_review(review):
    ''' fedireads json for book reviews '''
    status = get_status(review)
    status['inReplyToBook'] = review.book.absolute_id
    status['fedireadsType'] = review.status_type
    status['name'] = review.name
    status['rating'] = review.rating
    return status


def get_review_article(review):
    ''' a book review formatted for a non-fedireads isntance (mastodon) '''
    status = get_status(review)
    name = 'Review of "%s" (%d stars): %s' % (
        review.book.data['title'],
        review.rating,
        review.name
    )
    status['name'] = name
    return status


def get_status(status):
    ''' create activitypub json for a status '''
    user = status.user
    uri = status.absolute_id
    reply_parent_id = status.reply_parent.absolute_id \
        if status.reply_parent else None
    status_json = {
        'id': uri,
        'url': uri,
        'inReplyTo': reply_parent_id,
        'published': status.created_date.isoformat(),
        'attributedTo': user.actor,
        # TODO: assuming all posts are public -- should check privacy db field
        'to': ['https://www.w3.org/ns/activitystreams#Public'],
        'cc': ['%s/followers' % user.absolute_id],
        'sensitive': status.sensitive,
        'content': status.content,
        'type': status.activity_type,
        'attachment': [], # TODO: the book cover
        'replies': {
            'id': '%s/replies' % uri,
            'type': 'Collection',
            'first': {
                'type': 'CollectionPage',
                'next': '%s/replies?only_other_accounts=true&page=true' % uri,
                'partOf': '%s/replies' % uri,
                'items': [], # TODO: populate with replies
            }
        }
    }

    return status_json


def get_replies(status, replies):
    ''' collection of replies '''
    id_slug = status.absolute_id + '/replies'
    # TODO only partially implemented
    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': id_slug,
        'type': 'Collection',
        'first': {
            'id': '%s?page=true' % id_slug,
            'type': 'CollectionPage',
            'next': '%s?only_other_accounts=true&page=true' % id_slug,
            'partOf': id_slug,
            'items': [get_status(r) for r in replies]
        }
    }


def get_favorite(favorite):
    ''' like a post '''
    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': favorite.absolute_id,
        'type': 'Like',
        'actor': favorite.user.actor,
        'object': favorite.status.absolute_id,
    }


def get_add_tag(tag):
    ''' add activity for tagging a book '''
    uuid = uuid4()
    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': str(uuid),
        'type': 'Add',
        'actor': tag.user.actor,
        'object': {
            'type': 'Tag',
            'id': tag.absolute_id,
            'name': tag.name,
        },
        'target': {
            'type': 'Book',
            'id': tag.book.absolute_id,
        }
    }


def get_remove_tag(tag):
    ''' add activity for tagging a book '''
    uuid = uuid4()
    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': str(uuid),
        'type': 'Remove',
        'actor': tag.user.actor,
        'object': {
            'type': 'Tag',
            'id': tag.absolute_id,
            'name': tag.name,
        },
        'target': {
            'type': 'Book',
            'id': tag.book.absolute_id,
        }
    }



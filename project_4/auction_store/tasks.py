from celery import shared_task

from time import sleep


# @shared_task
# def end_auction():
#     result = add.apply_async((2, 2), countdown=7)
#     return result


# end_auction.get()
# @app.task
# def set_race_as_inactive(race_object):
#     """
#     This celery task sets the 'is_active' flag of the race object
#     to False in the database after the race end time has elapsed.
#     """

#     race_object.is_active = False # set the race as not active
#     race_object.save() # save the race object

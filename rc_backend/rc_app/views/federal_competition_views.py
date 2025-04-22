from rc_backend.rc_app.views.utils import force_post, force_get


@force_post
def create_federal_competition(request):
    pass


@force_post
def reject_regional_federal_competition_request(request):
    pass

@force_post
def accept_regional_federal_competition_request(request):
    pass

@force_get
def show_regional_federal_competition_request(request):
    pass
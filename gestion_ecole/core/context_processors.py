from catalog.models import School, SchoolYear

def active_context(request):
    sid = request.session.get("active_school_id")
    syid = request.session.get("active_schoolyear_id")
    school = School.objects.filter(id=sid).first() if sid else None
    sy = SchoolYear.objects.filter(id=syid).first() if syid else None
    return {"active_school": school, "active_school_year": sy}

import datetime
from django.views import generic
from .models import Tadameshi

# Create your views here.


class IndexView(generic.ListView):
    '''ホーム画面のビュー

    今回はこのビューしか使いませんが、何か要望があれば追加するかも？
    '''

    model = Tadameshi
    template_name = "hontai/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_list = Tadameshi.objects.filter(
            date=datetime.date.today()
        )
        next_list = Tadameshi.objects.filter(
            date__gt=datetime.date.today()
        ).order_by('date', 'time')
        
        try:
            recommend = Tadameshi.objects.get(
                date=datetime.date.today(),
                recommend=True
            )
            context['rec'] = recommend
        except:
            pass
        context['today_list'] = today_list
        context['next_list'] = next_list
        context['today'] = datetime.date.today()
        return context

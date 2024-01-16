from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.utils.decorators import method_decorator
from apps.hrdata.models import Document, Topic, Region, Tag
from apps.chat.models import SQLLog

 # Assuming the admin_required decorator is defined as shown earlier
from .decorators import admin_required  # Import the custom decorator


@method_decorator(admin_required, name='dispatch')
class TableView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Get the 'pk' from the URL kwargs
        document_id = kwargs.get('pk')
        if document_id:
            # Get a single document if 'pk' is provided
            context['document'] = get_object_or_404(Document, pk=document_id)
        else:
            # Get all documents if no specific 'pk' is provided
            context['documents'] = Document.objects.all()

        context['API_URL'] = settings.API_URL
        context['topics'] = Topic.objects.all()
        context['tags'] = Tag.objects.all()
        context['regions'] = Region.objects.all()
        context['documents'] = Document.objects.all()
        context['chatlogs'] = SQLLog.objects.all()
        return context

def document_update_view(request, pk):
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        # Process form data
        topic_id = request.POST.get('topic')
        tags_ids = request.POST.getlist('tags')
        region_id = request.POST.get('region')  # Retrieve region ID from form data
        content = request.POST.get('content')  # Retrieve document content from form data

        document.topic_id = topic_id
        document.tags.set(tags_ids)
        document.region_id = region_id
        document.content = content  # Update document content
        document.save()

        # Redirect to the document detail view
        return redirect('docs', pk=document.id)

    # Context for GET request
    context = {
        'document': document,
        'topics': Topic.objects.all(),
        'tags': Tag.objects.all(),
        'regions': Region.objects.all(),  # Add regions to the context
    }
    return render(request, 'doc.html', context)
from adrf.decorators import api_view
from adrf.views import APIView
from django.http import HttpRequest, JsonResponse

from .models import *
from drf_yasg.utils import swagger_auto_schema
from .serializers import response_serializers, request_serializers
from .my_example import get_response_examples


class TaskView(APIView):
    @swagger_auto_schema(
        query_serializer=request_serializers.GetTask,
        responses={
            '404': get_response_examples({'error': True, 'Error': 'Данной таски не существует'}),
            '200': get_response_examples(schema=response_serializers.TasksSerializer),
        },
        operation_summary='Получить задачу по id',
    )
    async def get(self, request, id):
        task = await Tasks.objects.filter(id=id).select_related('user').afirst()

        if task:
            data = response_serializers.TasksSerializer(task).data
            return JsonResponse(data, status=200)
        else:
            return JsonResponse({'error': True, 'Error': 'Данной таски не существует'}, status=404)

    @swagger_auto_schema(
        query_serializer=request_serializers.GetTask,
        responses={
            '404': get_response_examples({'error': True, 'Error': 'Данной таски не существует'}),
            '200': get_response_examples({'Info': 'Статус задачи успешно изменен на "undone"'}),
        },
        operation_summary='Обновить статус задачи',
    )
    async def patch(self, request, id):
        task = await Tasks.objects.filter(id=id).afirst()

        if task:
            task.status = 'undone'
            await task.asave()
            return JsonResponse({'Info': 'Статус задачи успешно изменен на "undone"'}, status=200)
        else:
            return JsonResponse({'error': True, 'Error': 'Данной таски не существует'}, status=404)

class TaskListView(APIView):
    @swagger_auto_schema(
        request_body=request_serializers.CreateTask,
        responses={
            '404': get_response_examples({'error': True, 'Error': 'Не все данные были переданы'}),
            '200': get_response_examples({'Info': 'Задача успешно создана'}),
        },
        operation_summary='Cоздать задачу',
    )
    async def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        tg_id = request.data.get('tg_id')
        deadline = request.data.get('deadline')

        if not title or not description or not tg_id:
            return JsonResponse({'error': True, 'Error': "Не все данные были переданы"}, status=404)

        user = await User.objects.filter(tg_id=tg_id).afirst()

        if user:
            await Tasks.objects.acreate(title=title, description=description, user=user, deadline=deadline)
            return JsonResponse({'Info': 'Задача успешно создана'}, status=200)
        else:
            return JsonResponse({'Error': 'Данного пользователя не существует'}, status=404)

    @swagger_auto_schema(
        query_serializer=request_serializers.TgId,
        responses={
            '404': get_response_examples({'error': True, 'Error': 'Данной таски не существует'}),
            '200': get_response_examples(schema=response_serializers.TasksSerializer),
        },
        operation_summary='Получить все задачи для пользователя',
    )
    async def get(self, request):
        tg_id = request.GET.get('telegram_user_id')

        user = await User.objects.filter(tg_id=tg_id).afirst()
        if user:
            all_tasks = [task async for task in Tasks.objects.filter(user=user).select_related('user').all()]
            data = response_serializers.TasksSerializer(all_tasks, many=True).data
            return JsonResponse(data, safe=False, status=200)
        else:
            return JsonResponse({'error': True, 'Error': 'Пользователя с таким "tg_id" не существует'}, status=404)
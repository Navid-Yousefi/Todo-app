def test_tasks_list_response_401(anon_client):

    response = anon_client.get('/tasks/tasks-list')
    assert response.status_code == 401


def test_tasks_list_response_200(auto_client):
    response = auto_client.get('/tasks/tasks-list')
    assert response.status_code == 200


def test_tasks_detail_response_200(auto_client, random_task):
    response = auto_client.get(
        "/tasks/detail",
        params={"task_id": random_task.id}
    )

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_tasks_detail_response_404(auto_client):
    response = auto_client.get('/tasks/detail/5454')
    assert response.status_code == 404

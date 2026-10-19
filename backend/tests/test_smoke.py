def test_app_imports():
    from app.main import app
    assert app is not None


def test_algorithm_modules_import():
    from app.algorithms import astar, bfs, dfs, iddfs
    assert all([astar, bfs, dfs, iddfs])
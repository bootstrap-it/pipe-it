import pipe_it

def test_pipe_it_1():
    assert [1, 2, 3] | pipe_it.first == 1
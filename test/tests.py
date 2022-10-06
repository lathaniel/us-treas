from src import ustreas


def test_unescape():
    assert ustreas.utils.unescape('test&lt;') == 'test<'
    assert ustreas.utils.unescape('&lt;test&lt;') == '<test<'
    assert ustreas.utils.unescape('&lt;test&lt;&gt;') == '<test<>'
    assert ustreas.utils.unescape('&lt;te&amp;&amp;st&lt;&gt;') == '<te&&st<>'

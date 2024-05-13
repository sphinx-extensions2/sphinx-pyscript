from sphinx_pytest.plugin import CreateDoctree


def test_basic(sphinx_doctree: CreateDoctree):
    sphinx_doctree.set_conf({"extensions": ["sphinx_pyscript"]})
    sphinx_doctree.buildername = "html"
    result = sphinx_doctree(
        """
Test
----

.. py-config::

    splashscreen:
        autoclose: true

.. py-editor::

.. py-script::

    print("Hello World")

    """
    )
    assert (
        [li.rstrip() for li in result.pformat().strip().splitlines()]
        == """
<document pyscript="True" source="<src>/index.rst">
    <section ids="test" names="test">
        <title>
            Test
        <raw format="html" xml:space="preserve">
            <script type="py-editor">

            </script>
        <raw format="html" xml:space="preserve">
            <py-terminal></py-terminal>
        <raw format="html" xml:space="preserve">
            <py-script>
            print("Hello World")
            </py-script>
    <raw format="html" xml:space="preserve">
        <py-config type="json">
        {
          "splashscreen": {
            "autoclose": true
          }
        }
        </py-config>
    """.strip().splitlines()
    )

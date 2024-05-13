.. py-config::

    splashscreen:
        autoclose: true
    packages:
    - matplotlib

Example with RST
================

`py-editor` and `py-terminal`
----------------------------

We can create an editor cell which will print `stdout`:

.. code-block:: restructuredtext

    .. py-editor::

        print("hallo world")
        import matplotlib.pyplot as plt
        plt.plot([1, 2, 3])
        plt.gcf()

Press `shift+enter` to run the code.

.. py-editor::

    print("hallo world")
    import matplotlib.pyplot as plt
    plt.plot([1, 2, 3])
    plt.gcf()

`py-script` application
-----------------------

Here is a simple application to replace "a" with "b", using the `py-script` directive:

.. code-block:: restructuredtext

    .. py-script::
        :file: convert_json_to_toml.py

    .. raw:: html

        <form method="post">
            <label for="input_text" style="display: block">Input</label>
            <textarea id="input_text" name="input_text" style="width: 90%">a</textarea>
            <label for="output_text" style="display: block">Output</label>
            <textarea id="output_text" name="output_text" readonly="true" style="width: 90%">b</textarea>
        </form>

With the following code:

.. literalinclude:: convert_json_to_toml.py
    :language: python

.. py-script::
    :file: convert_json_to_toml.py

.. raw:: html

    <form method="post">
        <label for="input_text" style="display: block">Input</label>
        <textarea id="input_text" name="input_text" style="width: 90%">a</textarea>
        <label for="output_text" style="display: block">Output</label>
        <textarea id="output_text" name="output_text" readonly="true" style="width: 90%">b</textarea>
    </form>

.. py-config::

    splashscreen:
        autoclose: true
    packages:
    - matplotlib

Example with RST
================

`py-repl` and `py-terminal`
----------------------------

We can create a REPL which will output to a `div` and print `stdout` to a terminal with:

.. code-block:: restructuredtext

    .. py-repl::
        :output: replOutput

        print("hallo world")
        import matplotlib.pyplot as plt
        plt.plot([1, 2, 3])
        plt.gcf()

    .. raw:: html

        <div id="replOutput"></div>

    .. py-terminal::

Press `shift+enter` to run the code.

.. py-repl::
    :output: replOutput

    print("hallo world")
    import matplotlib.pyplot as plt
    plt.plot([1, 2, 3])
    plt.gcf()

.. raw:: html

    <div id="replOutput"></div>

.. py-terminal::

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

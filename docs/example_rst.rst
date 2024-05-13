.. py-config::

    splashscreen:
        autoclose: true
    packages:
    - matplotlib

Example with RST
================

`py-editor` and `py-terminal`
----------------------------

We can create an editor cell which will print its `stdout`:

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

By default, each editor uses a separate copy of the Python interpreter. Code blocks with the same `env` (environment) share a copy of the Python interpreter:

.. code-block:: restructuredtext

    .. py-editor::
        :env: one

        x = 1

    .. py-editor::
        :env: one

        print(x)

    .. py-editor::
        :env: two

        print(x) # Error: x is not defined

Add the `setup` option to an editor tag in a given environment to include code that will run just before the first time the visible code in a block runs in that environment. Code in a `setup` block is invisible to the user. This is useful for setting up variables, imports, etc without cluttering up the editor cells.

.. code-block:: restructuredtext

    .. py-editor::
        :env: one
        :setup:

        # This code is not visible on the page
        from datetime import datetime

    .. py-editor::
        :env: one

        print(datetime.now())

Use the `config` option to specify the url of a `PyScript Configuration File <https://docs.pyscript.net/2024.5.2/user-guide/configuration/>`_:

.. code-block:: toml

    # config.toml
    packages = ['numpy', 'pandas']

.. code-block:: restructuredtext

    .. py-editor::
        :config: config.toml

        import numpy as np
        import pandas as pd

        s = pd.Series([1, 3, 5, np.nan, 6, 8])

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

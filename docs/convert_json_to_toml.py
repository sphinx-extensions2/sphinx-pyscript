from js import document

input_textarea = document.querySelector("form textarea#input_text")
output_textarea = document.querySelector("form textarea#output_text")


def do_convert(event):
    result = event.srcElement.value.replace("a", "b")
    output_textarea.value = result


input_textarea.oninput = do_convert


from prompt_toolkit import Application
from prompt_toolkit.widgets import RadioList, Dialog, Button
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout


def radiolist_prompt(
        src_list: list[tuple],
        default_value: str | None = None
):

    def handle_submit():
        app.exit()

    station_list = [(item['name'], item['name']) for item in src_list]

    radio_list = RadioList(station_list)

    dialog = Dialog(
        title="Select a Station",
        body=HSplit([radio_list]),
        buttons=[
            Button("Submit", handler=handle_submit)
        ],
        with_background=True
    )

    kb = KeyBindings()

    @kb.add("c-c")
    def _(event):
        app.exit()
        raise KeyboardInterrupt()

    app = Application(
        layout=Layout(dialog),
        key_bindings=kb,
        full_screen=True
    )

    app.run()

    return radio_list.current_value

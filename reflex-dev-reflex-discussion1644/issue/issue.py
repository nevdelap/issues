# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=redefined-outer-name

import reflex as rx


class Thing(rx.Base):
    value: str
    new_value: str | None
    is_editing: bool  # new_value is not None could serve this purpose, but to keep things clear.


class State(rx.State):
    things: list[Thing] = [
        Thing(
            value ="Hello from this example. 👋",
            new_value = None,
            is_editing=False
        ),
        Thing(
            value="The **other** thing.",
            new_value = None,
            is_editing=False
        ),
        Thing(
            value="And its friend.",
            new_value = None,
            is_editing=False
        ),
    ]

    def edit(self, index: int) -> None:
        self.things[index].new_value = self.things[index].value
        self.things[index].is_editing = True

    def update_new_value(self, index:int, value: str) -> None:
        self.things[index].new_value = value

    def save_edit(self, index: int) -> None:
        assert self.things[index].new_value is not None  # nosec
        self.things[index].value = str(self.things[index].new_value)  # str cast is because mypy can't figure out from the assert that it is not None.  # pylint: disable=line-too-long
        self.things[index].new_value = None
        self.things[index].is_editing = False

    def cancel_edit(self, index: int) -> None:
        self.things[index].new_value = None
        self.things[index].is_editing = False


def thing_box(thing: Thing, index: int) -> rx.Component:
    return rx.box(
        rx.cond(  # type: ignore
            # The issue: When this changes because of the the on_clicks below it
            # doesn't react, so you have to refresh the page to see the updated
            # state.
            thing.is_editing,
            rx.hstack(
                rx.debounce_input(
                    rx.input(
                        on_change=lambda value: State.update_new_value(index, value)  # type: ignore[call-arg,arg-type]  # pylint: disable=no-value-for-parameter
                    ),
                    value=thing.new_value,
                    debounce_timeout=250,
                ),
                rx.button(
                    rx.icon(tag="arrow_right"),
                    on_click=lambda: State.save_edit(index)  # type: ignore[attr-defined,call-arg,arg-type]  # pylint: disable=no-value-for-parameter,unknown-option-value
                ),
                rx.button(
                    rx.icon(tag="close"),
                    on_click=lambda: State.cancel_edit(index)  # type: ignore[attr-defined,call-arg,arg-type]  # pylint: disable=no-value-for-parameter,unknown-option-value
                ),
            ),
            rx.hstack(
                rx.box(
                    rx.markdown(
                        thing.value,
                    ),
                    background_color="#fafafa",
                    border_radius="10px",
                    padding="0.5em 1em 0.5em 1em",
                    width="100%",
                ),
                rx.button(
                    rx.icon(tag="edit"),
                    on_click=lambda: State.edit(index)  # type: ignore[attr-defined,call-arg,arg-type]  # pylint: disable=no-value-for-parameter,unknown-option-value
                )
            ),
        )
    )


def index() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.foreach(
                State.things,
                thing_box,
            ),
        ),
        align_items="center",
        display="flex",
        justify_content="center",
        min_height="100vh",
    )


app = rx.App() #state=State)
app.add_page(index)
app.compile()

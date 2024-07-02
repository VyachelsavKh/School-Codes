from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

class MyApp(App):
    def build(self):
        # Создаем корневой контейнер
        layout = FloatLayout()

        # Добавляем кнопку и устанавливаем её позицию и размер
        btn = Button(text="Hello Kivy",
                     size_hint=(None, None),
                     size=(200, 100),
                     pos=(10, 20))
        layout.add_widget(btn)

        return layout

if __name__ == '__main__':
    MyApp().run()
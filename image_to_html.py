def magic(name: str) -> str:
    return f"""<html>
    <head>
    <meta charset="UTF-8">
    <title>Це картинка</title>
    </head>
    <body>
    <p><img src={name} alt="Ну, не прогрузилась("</p>
    </body>
    <html>
    """

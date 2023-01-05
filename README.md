# literature clock

Clock using time quotes from a literature.

## Console

There is a shell script `litclock` that shows a quote for a current time:

> $ date
>
> Tue Dec 27 09:45:57 AM MSK 2022
>
> $ litclock
>
> "Первое, что бросилось нам в глаза, когда мы вошли в комнату Николауса,
> были стенные часы. Они показывали **без четверти десять**.
> Возможно ли, что ему оставалось так мало жить? Сердце у меня сжалось."
> -- 'Таинственный незнакомец', Марк Твен

## Web

The working site is in the `static/` folder, and can be visited at
https://bronevichok.ru/clock/. To run it locally you may need to serve `static/`
with an HTTP server (e.g. `python3 -m http.server`) ... or just open
`static/index.html` in a web browser.

## License

- English version: CC BY-NC-SA 2.5, [Johannes Enevoldsen](https://jenevoldsen.com/)
- Russian version: CC BY-NC-SA 2.5, [Sergey Bronnikov](https://bronevichok.ru/)

---
id: G-022
titulo: Auditoría de nuestras 9 miniaturas desde Drive > Miniaturas (segunda vuelta de G-017)
pedido: 2026-11-02
hilo: Operación autónoma de la tienda
herramienta: texto
entrega: doc
estado: pendiente
prioridad: normal
---
## Contexto
En G-017 no pudiste leer i.etsystatic.com. Claude subió las 9 fotos principales de nuestros listings a Drive, carpeta Gemini > Miniaturas (id 1QmAr8xSz_3eJ3sXQVpHWNUt8hhHZIQtR), a 570 px de ancho, el tamaño que sirve Etsy. Léelas con drive:download_file_content + view_file (o Pillow en el sandbox, reducidas a 170 px). Sin google:search ni browse.

## Qué quiero
Archivos (listing · producto · file_id):
- 4604988351 · Cold Case 01 · 1ERtSZgsgQksPGez1lvQCCN07wf6EaLdj
- 4605211787 · Cold Case 02 · 1uJP_ZOjcPzBNxIspKqmEyiDhd3r3exxZ
- 4605344156 · Cold Case 03 · 1sBi2sx4vZNeAOdFoXkVtjKtPlVwxbdJ9
- 4605344978 · Pack x3 Cold Case · 1AslucuBJdUku3zsVdBYo1tTA9nAXfEPu
- 4604404629 · Escape room de Navidad · 1IS6ztFpGohmM56RH0oFYm9Ikq86jT6RC
- 4603835971 · Trivia de películas · 1p_3i-oiDEMBxSa4NJmxJjLmUg1Q8si83
- 4605991888 · Piano villancicos · 1RHYukATsPkkgWk20IEf_xJabXyOr4OVF
- 4605993316 · Piano villancicos niños · 1CH-c_JzmaEuwuueCvWU09b_oGOdaQQLE
- 4605998382 · Piano clásicos fáciles · 1QzXS4VqB2pDga0y2mlgojkanyO9EI-FF
1. Confirma primero que pudiste abrir y VER la primera imagen (describe en una línea qué hay). Si no puedes, `estado: no-puedo` con el mensaje exacto.
2. Para cada imagen, cómo se ve en la grilla de Etsy en el teléfono (cuadrado ~170 px, Etsy recorta los bordes): qué texto se lee y cuál no, qué elemento domina, si hay algo que compita con el producto, nota del 1 al 10 como miniatura que hace clic.
3. Ordena las 9 de mejor a peor y da 3 cambios concretos y baratos (que Claude pueda hacer con Pillow o Remotion, sin diseñador) para la peor tercia.
4. Extra si queda cupo: con Pillow en el sandbox, reduce las 9 a 170x170 (recorte central), móntalas en una sola grilla 3x3 PNG y súbela a Entregas como `G-022 grilla 170px.png`; así Claude ve lo mismo que tú.

## Formato de la respuesta
Español. Doc `G-022 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas; tabla (listing | producto | se_lee | domina | nota | cambio). Máximo 1.500 palabras.

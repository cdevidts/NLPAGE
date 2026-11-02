---
id: G-017
titulo: Sonda: leer nuestras fotos principales desde el CDN de Etsy y auditarlas como miniaturas
pedido: 2026-11-01
hilo: Operación autónoma de la tienda
herramienta: navegar
entrega: doc
estado: pendiente
---
## Contexto
En G-013 propusiste auditar nuestras miniaturas si te damos las imágenes. Las fotos principales de los listings están en el CDN de Etsy (i.etsystatic.com), que no es la página de Etsy: queremos saber si lo puedes leer. Primero una sonda, después la auditoría. Sin google:search; como máximo 9 llamadas a google:browse.

## Qué quiero
1. Sonda: intenta abrir con google:browse la primera URL de la lista. Si devuelve la imagen (o te deja describirla), sigue con las demás; si está bloqueada, `estado: no-puedo` con el mensaje exacto y termina (no insistas).
2. Si se ven: para cada imagen, descríbela como se vería en la grilla de Etsy en el teléfono (cuadrado de ~170 px): qué se lee, qué no se lee, qué elemento domina, si el precio/badge compite con el producto, y nota del 1 al 10 como miniatura que hace clic. Luego ordena las 9 de mejor a peor y da 3 cambios concretos para la peor tercia.
Listado (listing · producto · URL):
- 4604988351 · Cold Case 01 · https://i.etsystatic.com/68748133/r/il/62d446/8805598391/il_570xN.8805598391_d6js.jpg
- 4605211787 · Cold Case 02 · https://i.etsystatic.com/68748133/r/il/391ee2/8807384983/il_570xN.8807384983_g0vn.jpg
- 4605344156 · Cold Case 03 · https://i.etsystatic.com/68748133/r/il/f6ec44/8808266165/il_570xN.8808266165_sx78.jpg
- 4605344978 · Pack x3 Cold Case · https://i.etsystatic.com/68748133/r/il/e4d4ed/8808272787/il_570xN.8808272787_o9eg.jpg
- 4604404629 · Escape room de Navidad · https://i.etsystatic.com/68748133/r/il/2d8582/8752885934/il_570xN.8752885934_2f3r.jpg
- 4603835971 · Trivia de películas · https://i.etsystatic.com/68748133/r/il/15c6cc/8795735523/il_570xN.8795735523_l3ex.jpg
- 4605991888 · Piano villancicos · https://i.etsystatic.com/68748133/r/il/f5c808/8813583333/il_570xN.8813583333_q0r5.jpg
- 4605993316 · Piano villancicos niños · https://i.etsystatic.com/68748133/r/il/81fb8d/8813594161/il_570xN.8813594161_mlez.jpg
- 4605998382 · Piano clásicos fáciles · https://i.etsystatic.com/68748133/r/il/eec3bf/8813632209/il_570xN.8813632209_kuzk.jpg

## Formato de la respuesta
Español. Doc `G-017 RESPUESTA` con estado, fecha y modelo en las 3 primeras líneas; tabla (listing | producto | se_lee | domina | nota | cambio). Máximo 1.500 palabras.

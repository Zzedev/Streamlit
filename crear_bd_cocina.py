# setup_cocina_min.py
import sqlite3
import unicodedata

def remove_accents(text: str) -> str:
    nfkd = unicodedata.normalize('NFKD', text)
    ascii_text = "".join(c for c in nfkd if not unicodedata.combining(c))
    return ascii_text.replace('ñ', 'n').replace('Ñ', 'N').lower().strip()

# Lista de palabras relacionadas con cocina (en versión original)
palabras_cocina = [
"freir","hervir","hornear","asar","brasear","saltear","sudar","confitar","flambear","gratinar",
"escalfar","vapor","estofar","reducir","sellar","pochar","fundir","glasear","marinar","ahumar",
"desglasar","dorar","templar","licuar","triturar","amasar","batir","tamizar","colar","mezclar",
"sarten","olla","cuchillo","tenedor","cuchara","batidor","licuadora","horno","microondas","tabla",
"colador","rallador","espumadera","pinzas","cazo","rodillo","molinillo","mortero","pistilo","wok",
"cacerola","parrilla","plancha","vaporera","freidora","pelador","abrelatas","tijeras","pincho","brocha",
"sal","azucar","harina","huevo","leche","mantequilla","manteca","aceite","vinagre","agua",
"arroz","pasta","pimienta","ajo","cebolla","tomate","chile","pan","levadura","queso",
"crema","yogur","limon","mostaza","mayonesa","catsup","soya","miel","chocolate","cacao",
"vainilla","canela","caramelo","dulce","salado","amargo","acido","picante","ahumado","agridulce",
"pollo","res","cerdo","cordero","jamon","tocino","costilla","filete","chuleta","bistec",
"arrachera","picana","longaniza","chorizo","salchicha","pavo","conejo","cabrito","carne","molida",
"pescado","atun","salmon","camaron","pulpo","calamar","tilapia","bacalao","jaiba","langosta",
"almeja","ostion","mejillon","mojarra","sardina","trucha","mero","robalo","pez","marisco",
"zanahoria","papa","lechuga","pepino","brocoli","coliflor","espinaca","champinon","calabaza","berenjena",
"chayote","repollo","nopal","ejote","cebollin","apio","betabel","rabano","elote","jitomate",
"manzana","pera","platano","fresa","mango","pina","uva","naranja","papaya","sandia",
"melon","durazno","guayaba","ciruela","kiwi","toronja","coco","mandarina","limon","fruta",
"salsa","mole","guacamole","vinagreta","pesto","chimichurri","adobo","sofrito","pure","coulis",
"bechamel","holandesa","ragu","demiglace","veloute","fumet","fond","reduccion","emulsion","espuma",
"pan","pastel","galleta","bizcocho","brownie","cupcake","dona","tarta","pie","postre",
"flan","gelatina","natilla","tiramisu","cheesecake","helado","sorbet","paleta","reposteria","panaderia",
"juliana","brunoise","chiffonade","rodaja","filetear","rebanar","trocear","desmenuzar","picar","moler",
"laminar","cubear","reducir","colar","montar","ligar","emulsionar","textura","corte","porcion",
"oregano","tomillo","romero","laurel","albahaca","clavo","nuezmoscada","comino","curcuma","cardamomo",
"anis","cilantro","eneldo","perejil","hierbabuena","sesamo","paprika","curry","jengibre","chilepolvo",
"taco","tamale","enchilada","pozole","menudo","barbacoa","birria","tostada","quesadilla","sopa",
"consome","caldo","paella","lasagna","pizza","hamburguesa","hotdog","sushi","ramen","ceviche",
"cafe","te","limonada","licuado","batido","vino","cerveza","coctel","smoothie","atole",
"chocolatecaliente","aguafresca","malteada","sidra","champana","sake","ron","tequila","mezcal","bebida",
"menu","receta","ingrediente","porcion","servicio","presentacion","emplatar","degustar","catar","sabor",
"textura","aroma","cocina","chef","cocinero","ayudante","brigada","linea","turno","servicio",
"restaurante","bistro","cafeteria","comedor","buffet","banquete","evento","catering","reserva","mesa",
"desayuno","comida","cena","snack","entrada","plato","fuerte","guarnicion","ensalada","sopa",
"maridaje","degustacion","temporada","producto","local","fresco","organico","natural","congelado","seco",
"enlatado","ahumado","curado","salado","dulce","amargo","acido","picante","umami","neutro",
"crudo","cocido","grill","rostizado","salteado","frito","horneado","vaporizado","sellado","estofado",
"crocante","suave","cremoso","jugoso","seco","tierno","duro","ligero","pesado","denso",
"platoondo","platoplano","platohondo","vaso","taza","copa","jarra","botella","charola","bandeja",
"mantel","servilleta","cubierto","copa","salero","pimentero","aceitera","vinagrera","palillo","popote",
"almacen","despensa","refrigerador","congelador","estante","recipiente","tapa","frasco","bolsa","envase",
"fecha","caducidad","lote","higiene","limpieza","sanitizar","desinfectar","seguridad","salubridad","norma",
"porcionado","gramaje","kilogramo","litro","mililitro","onza","libra","taza","cucharada","cucharadita",
"temperatura","tiempo","reloj","control","proceso","tecnica","metodo","sistema","flujo","rutina",
"proveedor","insumo","pedido","entrega","factura","costo","precio","venta","ganancia","perdida",
"cliente","comensal","opinion","resena","satisfaccion","calidad","excelencia","servicio","rapidez","atencion",
"menuinfantil","dietas","vegano","vegetariano","keto","light","sinazucar","singluten","organico","integral",
"fermento","masa","cultivo","levadura","bacteria","probio tico","curado","reposo","maduracion","reposado",
"acero","teflon","ceramica","vidrio","madera","plastico","aluminio","hierro","cobre","material",
"cocinafria","cocinacaliente","cocinamexicana","cocinaitaliana","cocinaasiatica",
"cocinamediterranea","cocinavegana","cocinafusion","gastronomia","gastronomo"
]

# Normalizamos: quitamos acentos, convertimos a minúsculas
palabras_sin_acentos = [remove_accents(p) for p in palabras_cocina]

# Eliminamos duplicados (por si hay "béchamel" y "bechamel")
palabras_sin_acentos = list(dict.fromkeys(palabras_sin_acentos))

# Guardamos en SQLite
conn = sqlite3.connect("cocina.db")
cursor = conn.cursor()

# Crear tabla limpia
cursor.execute("DROP TABLE IF EXISTS palabras")
cursor.execute("CREATE TABLE palabras (palabra TEXT PRIMARY KEY)")

# Insertar
cursor.executemany("INSERT OR IGNORE INTO palabras (palabra) VALUES (?)", 
                   [(p,) for p in palabras_sin_acentos])

conn.commit()
conn.close()

print("✅ cocina.db creado con", len(palabras_sin_acentos), "palabras (sin acentos).")
print("Ejemplos:", palabras_sin_acentos[:10])
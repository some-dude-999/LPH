#!/usr/bin/env python3
"""
Generate Spanish Example Words for SpanishWordsOverview.csv
Each base word gets 2 example phrases that CONTAIN that base word.
"""

import csv
import re

def parse_word_list(words_str):
    """Parse [word1,word2,...] format to list."""
    words_content = words_str.strip()[1:-1]  # Remove [ and ]
    return [w.strip() for w in words_content.split(',')]

def format_word_list(words):
    """Format list as [word1,word2,...] string."""
    return '[' + ','.join(words) + ']'

# Example generators - creating 2 natural phrases containing each word
def generate_examples(word, pack_title):
    """Generate 2 example phrases containing the given word."""

    word_lower = word.lower()

    # Dictionary of curated examples for better quality
    examples = {
        # Pack 1: Greetings & Goodbyes
        'hola': ['hola amigo', 'hola señora'],
        'adiós': ['adiós amigos', 'decir adiós'],
        'buenos días': ['muy buenos días', 'buenos días señor'],
        'buenas tardes': ['muy buenas tardes', 'buenas tardes a todos'],
        'buenas noches': ['muy buenas noches', 'buenas noches señora'],
        'por favor': ['ayuda por favor', 'por favor espera'],
        'gracias': ['muchas gracias', 'gracias amigo'],
        'de nada': ['es de nada', 'de nada señor'],
        'perdón': ['perdón señor', 'pido perdón'],
        'disculpe': ['disculpe señor', 'disculpe la molestia'],
        'con permiso': ['con permiso paso', 'con permiso señora'],
        'hasta luego': ['nos vemos hasta luego', 'hasta luego amigo'],
        'hasta mañana': ['nos vemos hasta mañana', 'hasta mañana amigos'],
        'bienvenido': ['muy bienvenido aquí', 'bienvenido a casa'],
        'bienvenida': ['muy bienvenida aquí', 'bienvenida a casa'],

        # Pack 2: Yes No & Agreement
        'sí': ['sí claro', 'sí señor'],
        'no': ['no gracias', 'no sé'],
        'tal vez': ['tal vez mañana', 'tal vez sí'],
        'quizás': ['quizás mañana', 'quizás sí'],
        'claro': ['claro que sí', 'claro señor'],
        'por supuesto': ['por supuesto que sí', 'por supuesto señora'],
        'vale': ['vale perfecto', 'vale de acuerdo'],
        'está bien': ['está bien gracias', 'todo está bien'],
        'de acuerdo': ['estoy de acuerdo', 'de acuerdo contigo'],
        'correcto': ['muy correcto', 'es correcto'],

        # Pack 3: Numbers 0-10
        'cero': ['número cero', 'tengo cero'],
        'uno': ['número uno', 'tengo uno'],
        'dos': ['número dos', 'tengo dos'],
        'tres': ['número tres', 'tengo tres'],
        'cuatro': ['número cuatro', 'tengo cuatro'],
        'cinco': ['número cinco', 'tengo cinco'],
        'seis': ['número seis', 'tengo seis'],
        'siete': ['número siete', 'tengo siete'],
        'ocho': ['número ocho', 'tengo ocho'],
        'nueve': ['número nueve', 'tengo nueve'],
        'diez': ['número diez', 'tengo diez'],

        # Pack 4: Question Words
        'qué': ['qué pasa', 'qué quieres'],
        'quién': ['quién es', 'quién sabe'],
        'dónde': ['dónde está', 'dónde vives'],
        'cuándo': ['cuándo vienes', 'cuándo es'],
        'por qué': ['por qué no', 'dime por qué'],
        'cómo': ['cómo estás', 'cómo te llamas'],
        'cuál': ['cuál prefieres', 'cuál es'],
        'cuánto': ['cuánto cuesta', 'cuánto tiempo'],
        'cuánta': ['cuánta agua', 'cuánta gente'],
        'cuántos': ['cuántos años', 'cuántos tienes'],
        'cuántas': ['cuántas personas', 'cuántas veces'],

        # Pack 5: Personal Pronouns
        'yo': ['yo soy', 'yo quiero'],
        'tú': ['tú eres', 'tú sabes'],
        'él': ['él es', 'él tiene'],
        'ella': ['ella es', 'ella tiene'],
        'usted': ['usted es', 'usted tiene'],
        'nosotros': ['nosotros somos', 'nosotros vamos'],
        'nosotras': ['nosotras somos', 'nosotras vamos'],
        'vosotros': ['vosotros sois', 'vosotros tenéis'],
        'vosotras': ['vosotras sois', 'vosotras tenéis'],
        'ellos': ['ellos son', 'ellos tienen'],
        'ellas': ['ellas son', 'ellas tienen'],
        'ustedes': ['ustedes son', 'ustedes tienen'],

        # Pack 6: Ser (to be permanent)
        'ser': ['quiero ser', 'puede ser'],
        'soy': ['yo soy feliz', 'soy estudiante'],
        'eres': ['tú eres bueno', 'eres mi amigo'],
        'es': ['él es alto', 'es importante'],
        'somos': ['nosotros somos amigos', 'somos estudiantes'],
        'sois': ['vosotros sois buenos', 'sois amigos'],
        'son': ['ellos son amigos', 'son estudiantes'],
        'profesión': ['mi profesión es', 'buena profesión'],
        'nacionalidad': ['mi nacionalidad es', 'tu nacionalidad'],
        'personalidad': ['su personalidad es', 'buena personalidad'],
        'inteligente': ['muy inteligente', 'es inteligente'],
        'simpático': ['muy simpático', 'es simpático'],
        'trabajador': ['muy trabajador', 'es trabajador'],
        'honesto': ['muy honesto', 'es honesto'],
        'amable': ['muy amable', 'es amable'],

        # Pack 7: Estar (to be temporary)
        'estar': ['voy a estar', 'puede estar'],
        'estoy': ['estoy bien', 'estoy aquí'],
        'estás': ['cómo estás', 'estás bien'],
        'está': ['dónde está', 'está aquí'],
        'estamos': ['estamos listos', 'estamos aquí'],
        'estáis': ['estáis bien', 'estáis aquí'],
        'están': ['ellos están bien', 'están aquí'],
        'ubicación': ['la ubicación es', 'buena ubicación'],
        'condición': ['en buena condición', 'la condición es'],
        'ánimo': ['buen ánimo', 'con ánimo'],
        'enfermo': ['estoy enfermo', 'está enfermo'],
        'ocupado': ['estoy ocupado', 'está ocupado'],
        'cansado': ['estoy cansado', 'está cansado'],
        'abierto': ['está abierto', 'siempre abierto'],
        'situado': ['está situado aquí', 'bien situado'],

        # Pack 8: Tener (to have)
        'tengo': ['tengo hambre', 'tengo tiempo'],
        'tienes': ['tienes razón', 'tienes tiempo'],
        'tiene': ['él tiene casa', 'tiene tiempo'],
        'tenemos': ['tenemos tiempo', 'tenemos hambre'],
        'tenéis': ['tenéis razón', 'tenéis tiempo'],
        'tienen': ['ellos tienen casa', 'tienen tiempo'],
        'tener': ['voy a tener', 'debe tener'],
        'hambre': ['hay hambre', 'mucha hambre'],
        'sed': ['tengo sed', 'mucha sed'],
        'sueño': ['tengo sueño', 'mucho sueño'],
        'miedo': ['tengo miedo', 'mucho miedo'],
        'prisa': ['tengo prisa', 'mucha prisa'],
        'razón': ['la razón es', 'con razón'],
        'suerte': ['buena suerte', 'tengo suerte'],

        # Pack 9: Articles
        'el': ['el libro', 'el hombre'],
        'la': ['la casa', 'la mujer'],
        'los': ['los libros', 'los hombres'],
        'las': ['las casas', 'las mujeres'],
        'un': ['un libro', 'un hombre'],
        'una': ['una casa', 'una mujer'],
        'unos': ['unos libros', 'unos hombres'],
        'unas': ['unas casas', 'unas mujeres'],

        # Pack 10: Connecting Words
        'y': ['tú y yo', 'pan y agua'],
        'o': ['sí o no', 'uno o dos'],
        'pero': ['quiero pero no puedo', 'pero no sé'],
        'porque': ['porque quiero', 'porque sí'],
        'si': ['si quieres', 'si puedes'],
        'cuando': ['cuando quieras', 'cuando puedas'],
        'donde': ['donde quieras', 'donde está'],
        'así': ['así es', 'así está bien'],
        'también': ['yo también', 'también quiero'],
        'tampoco': ['yo tampoco', 'tampoco sé'],

        # Pack 11: Days
        'lunes': ['el lunes', 'cada lunes'],
        'martes': ['el martes', 'cada martes'],
        'miércoles': ['el miércoles', 'cada miércoles'],
        'jueves': ['el jueves', 'cada jueves'],
        'viernes': ['el viernes', 'cada viernes'],
        'sábado': ['el sábado', 'cada sábado'],
        'domingo': ['el domingo', 'cada domingo'],
        'día': ['cada día', 'buen día'],
        'semana': ['esta semana', 'cada semana'],
        'fin': ['el fin de semana', 'sin fin'],

        # Pack 12: Months
        'enero': ['en enero', 'primero de enero'],
        'febrero': ['en febrero', 'catorce de febrero'],
        'marzo': ['en marzo', 'primero de marzo'],
        'abril': ['en abril', 'primero de abril'],
        'mayo': ['en mayo', 'cinco de mayo'],
        'junio': ['en junio', 'primero de junio'],
        'julio': ['en julio', 'cuatro de julio'],
        'agosto': ['en agosto', 'primero de agosto'],
        'septiembre': ['en septiembre', 'primero de septiembre'],
        'octubre': ['en octubre', 'primero de octubre'],
        'noviembre': ['en noviembre', 'primero de noviembre'],
        'diciembre': ['en diciembre', 'veinticinco de diciembre'],
        'mes': ['este mes', 'cada mes'],
        'año': ['este año', 'cada año'],

        # Pack 13: Family
        'familia': ['mi familia', 'la familia'],
        'padre': ['mi padre', 'el padre'],
        'madre': ['mi madre', 'la madre'],
        'hijo': ['mi hijo', 'el hijo'],
        'hija': ['mi hija', 'la hija'],
        'hermano': ['mi hermano', 'el hermano'],
        'hermana': ['mi hermana', 'la hermana'],
        'abuelo': ['mi abuelo', 'el abuelo'],
        'abuela': ['mi abuela', 'la abuela'],
        'tío': ['mi tío', 'el tío'],
        'tía': ['mi tía', 'la tía'],
        'primo': ['mi primo', 'el primo'],
        'prima': ['mi prima', 'la prima'],
        'esposo': ['mi esposo', 'el esposo'],
        'esposa': ['mi esposa', 'la esposa'],

        # Pack 14: Body Parts
        'cabeza': ['mi cabeza', 'la cabeza duele'],
        'cara': ['tu cara', 'la cara'],
        'ojo': ['el ojo', 'mi ojo'],
        'oreja': ['la oreja', 'mi oreja'],
        'nariz': ['la nariz', 'mi nariz'],
        'boca': ['la boca', 'mi boca'],
        'diente': ['el diente', 'mi diente'],
        'lengua': ['la lengua', 'mi lengua'],
        'cuello': ['el cuello', 'mi cuello'],
        'hombro': ['el hombro', 'mi hombro'],
        'brazo': ['el brazo', 'mi brazo'],
        'mano': ['la mano', 'mi mano'],
        'dedo': ['el dedo', 'mi dedo'],
        'pecho': ['el pecho', 'mi pecho'],
        'espalda': ['la espalda', 'mi espalda'],
        'estómago': ['el estómago', 'mi estómago'],
        'pierna': ['la pierna', 'mi pierna'],
        'rodilla': ['la rodilla', 'mi rodilla'],
        'pie': ['el pie', 'mi pie'],

        # Pack 15: Colors
        'rojo': ['color rojo', 'es rojo'],
        'azul': ['color azul', 'es azul'],
        'verde': ['color verde', 'es verde'],
        'amarillo': ['color amarillo', 'es amarillo'],
        'negro': ['color negro', 'es negro'],
        'blanco': ['color blanco', 'es blanco'],
        'gris': ['color gris', 'es gris'],
        'marrón': ['color marrón', 'es marrón'],
        'naranja': ['color naranja', 'es naranja'],
        'rosa': ['color rosa', 'es rosa'],
        'morado': ['color morado', 'es morado'],
        'oscuro': ['azul oscuro', 'color oscuro'],
        'turquesa': ['color turquesa', 'es turquesa'],

        # Pack 16: Describing Things
        'grande': ['muy grande', 'es grande'],
        'pequeño': ['muy pequeño', 'es pequeño'],
        'alto': ['muy alto', 'es alto'],
        'flaco': ['muy flaco', 'es flaco'],
        'largo': ['muy largo', 'es largo'],
        'corto': ['muy corto', 'es corto'],
        'ancho': ['muy ancho', 'es ancho'],
        'estrecho': ['muy estrecho', 'es estrecho'],
        'nuevo': ['muy nuevo', 'es nuevo'],
        'viejo': ['muy viejo', 'es viejo'],
        'joven': ['muy joven', 'es joven'],
        'bueno': ['muy bueno', 'es bueno'],
        'malo': ['muy malo', 'es malo'],
        'fácil': ['muy fácil', 'es fácil'],
        'difícil': ['muy difícil', 'es difícil'],
        'rápido': ['muy rápido', 'es rápido'],
        'lento': ['muy lento', 'es lento'],
        'bonito': ['muy bonito', 'es bonito'],
        'feo': ['muy feo', 'es feo'],

        # Pack 17: Basic Action Verbs
        'venir': ['puede venir', 'quiero venir'],
        'tomar': ['voy a tomar', 'puedo tomar'],
        'hablar': ['voy a hablar', 'puedo hablar'],
        'ver': ['voy a ver', 'puedo ver'],
        'oír': ['puedo oír', 'quiero oír'],
        'entrar': ['puedo entrar', 'voy a entrar'],
        'comer': ['voy a comer', 'quiero comer'],
        'nacer': ['acaba de nacer', 'va a nacer'],
        'reír': ['me hace reír', 'quiero reír'],
        'llorar': ['no quiero llorar', 'va a llorar'],
        'gritar': ['no quiero gritar', 'va a gritar'],
        'trabajar': ['tengo que trabajar', 'voy a trabajar'],
        'ayudar': ['puedo ayudar', 'quiero ayudar'],
        'conversar': ['vamos a conversar', 'quiero conversar'],
        'limpiar': ['tengo que limpiar', 'voy a limpiar'],

        # Pack 18: Common Foods
        'comida': ['la comida', 'buena comida'],
        'agua': ['el agua', 'beber agua'],
        'pan': ['el pan', 'comer pan'],
        'leche': ['la leche', 'beber leche'],
        'café': ['el café', 'tomar café'],
        'té': ['el té', 'tomar té'],
        'fruta': ['la fruta', 'comer fruta'],
        'manzana': ['una manzana', 'la manzana'],
        'plátano': ['un plátano', 'el plátano'],
        'arroz': ['el arroz', 'comer arroz'],
        'pasta': ['la pasta', 'comer pasta'],
        'carne': ['la carne', 'comer carne'],
        'pollo': ['el pollo', 'comer pollo'],
        'pescado': ['el pescado', 'comer pescado'],
        'huevos': ['los huevos', 'comer huevos'],
        'queso': ['el queso', 'comer queso'],
        'ensalada': ['la ensalada', 'comer ensalada'],
        'tomate': ['el tomate', 'el tomate rojo'],
        'patatas': ['las patatas', 'comer patatas'],
        'galleta': ['una galleta', 'la galleta'],

        # Pack 19: House Rooms
        'casa': ['mi casa', 'en casa'],
        'apartamento': ['mi apartamento', 'el apartamento'],
        'habitación': ['la habitación', 'mi habitación'],
        'baño': ['el baño', 'ir al baño'],
        'salón': ['el salón', 'en el salón'],
        'dormitorio': ['el dormitorio', 'mi dormitorio'],
        'comedor': ['el comedor', 'en el comedor'],
        'jardín': ['el jardín', 'en el jardín'],
        'puerta': ['la puerta', 'abrir la puerta'],
        'ventana': ['la ventana', 'abrir la ventana'],
        'pared': ['la pared', 'en la pared'],
        'techo': ['el techo', 'bajo el techo'],
        'suelo': ['el suelo', 'en el suelo'],
        'escaleras': ['las escaleras', 'subir escaleras'],
        'garaje': ['el garaje', 'en el garaje'],

        # Pack 20: Hacer (to do/make)
        'hacer': ['voy a hacer', 'puedo hacer'],
        'hago': ['yo hago', 'lo hago'],
        'haces': ['qué haces', 'tú haces'],
        'hace': ['qué hace', 'él hace'],
        'hacemos': ['lo hacemos', 'nosotros hacemos'],
        'hacéis': ['qué hacéis', 'lo hacéis'],
        'hacen': ['qué hacen', 'ellos hacen'],
        'tarea': ['la tarea', 'hacer tarea'],
        'cama': ['la cama', 'hacer la cama'],
        'cola': ['hacer cola', 'la cola'],
        'ejercicio': ['hacer ejercicio', 'el ejercicio'],
        'deporte': ['hacer deporte', 'el deporte'],
        'planes': ['hacer planes', 'los planes'],
        'caso': ['hacer caso', 'en todo caso'],
        'daño': ['hacer daño', 'sin daño'],
        'ruido': ['hacer ruido', 'mucho ruido'],
        'esfuerzo': ['hacer esfuerzo', 'con esfuerzo'],

        # Pack 21: Ir (to go)
        'ir': ['voy a ir', 'quiero ir'],
        'voy': ['yo voy', 'voy a casa'],
        'vas': ['adónde vas', 'tú vas'],
        'va': ['él va', 'ella va'],
        'vamos': ['nosotros vamos', 'vamos a casa'],
        'vais': ['adónde vais', 'vosotros vais'],
        'van': ['ellos van', 'van a casa'],
        'destino': ['el destino', 'mi destino'],
        'dirección': ['la dirección', 'buena dirección'],
        'camino': ['el camino', 'en camino'],
        'ruta': ['la ruta', 'nueva ruta'],
        'paseo': ['el paseo', 'dar un paseo'],
        'visita': ['la visita', 'una visita'],
        'excursión': ['la excursión', 'una excursión'],
        'trayecto': ['el trayecto', 'largo trayecto'],

        # Pack 22: Numbers 11-20
        'once': ['número once', 'son las once'],
        'doce': ['número doce', 'son las doce'],
        'trece': ['número trece', 'tengo trece'],
        'catorce': ['número catorce', 'tengo catorce'],
        'quince': ['número quince', 'tengo quince'],
        'dieciséis': ['número dieciséis', 'tengo dieciséis'],
        'diecisiete': ['número diecisiete', 'tengo diecisiete'],
        'dieciocho': ['número dieciocho', 'tengo dieciocho'],
        'diecinueve': ['número diecinueve', 'tengo diecinueve'],
        'veinte': ['número veinte', 'tengo veinte'],

        # Pack 23: Extended Family
        'novio': ['mi novio', 'el novio'],
        'novia': ['mi novia', 'la novia'],
        'marido': ['mi marido', 'el marido'],
        'mujer': ['mi mujer', 'la mujer'],
        'bebé': ['el bebé', 'un bebé'],
        'niño': ['el niño', 'un niño'],
        'niña': ['la niña', 'una niña'],
        'adulto': ['un adulto', 'el adulto'],
        'adulta': ['una adulta', 'la adulta'],
        'padres': ['mis padres', 'los padres'],
        'hijos': ['mis hijos', 'los hijos'],
        'abuelos': ['mis abuelos', 'los abuelos'],
        'nietos': ['mis nietos', 'los nietos'],
        'pariente': ['un pariente', 'el pariente'],
        'parienta': ['una parienta', 'la parienta'],

        # Pack 24: Emotions & Feelings
        'feliz': ['estoy feliz', 'muy feliz'],
        'triste': ['estoy triste', 'muy triste'],
        'enojado': ['estoy enojado', 'muy enojado'],
        'preocupado': ['estoy preocupado', 'muy preocupado'],
        'aburrido': ['estoy aburrido', 'muy aburrido'],
        'emocionado': ['estoy emocionado', 'muy emocionado'],
        'nervioso': ['estoy nervioso', 'muy nervioso'],
        'tranquilo': ['estoy tranquilo', 'muy tranquilo'],
        'contento': ['estoy contento', 'muy contento'],
        'asustado': ['estoy asustado', 'muy asustado'],
        'sorprendido': ['estoy sorprendido', 'muy sorprendido'],
        'confundido': ['estoy confundido', 'muy confundido'],
        'frustrado': ['estoy frustrado', 'muy frustrado'],
        'avergonzado': ['estoy avergonzado', 'muy avergonzado'],
        'aliviado': ['estoy aliviado', 'muy aliviado'],
        'satisfecho': ['estoy satisfecho', 'muy satisfecho'],

        # Pack 25: Time Words
        'hoy': ['para hoy', 'hoy día'],
        'ayer': ['fue ayer', 'desde ayer'],
        'mañana': ['hasta mañana', 'mañana temprano'],
        'ahora': ['ahora mismo', 'desde ahora'],
        'tarde': ['por la tarde', 'más tarde'],
        'después': ['después de', 'hasta después'],
        'antes': ['antes de', 'mucho antes'],
        'siempre': ['como siempre', 'para siempre'],
        'nunca': ['nunca más', 'casi nunca'],
        'a veces': ['a veces sí', 'solo a veces'],
        'todavía': ['todavía no', 'todavía más'],
        'ya': ['ya está', 'ya no'],
        'temprano': ['muy temprano', 'demasiado temprano'],
        'vez': ['una vez', 'otra vez'],
        'pronto': ['muy pronto', 'hasta pronto'],

        # Pack 26: Clothing
        'ropa': ['la ropa', 'mi ropa'],
        'camisa': ['la camisa', 'mi camisa'],
        'camiseta': ['la camiseta', 'mi camiseta'],
        'pantalones': ['los pantalones', 'mis pantalones'],
        'vestido': ['el vestido', 'mi vestido'],
        'falda': ['la falda', 'mi falda'],
        'zapatos': ['los zapatos', 'mis zapatos'],
        'calcetines': ['los calcetines', 'mis calcetines'],
        'chaqueta': ['la chaqueta', 'mi chaqueta'],
        'abrigo': ['el abrigo', 'mi abrigo'],
        'sombrero': ['el sombrero', 'mi sombrero'],
        'gorra': ['la gorra', 'mi gorra'],
        'guantes': ['los guantes', 'mis guantes'],
        'cinturón': ['el cinturón', 'mi cinturón'],
        'corbata': ['la corbata', 'mi corbata'],

        # Pack 27: Daily Activities
        'como': ['yo como', 'como bien'],
        'bebo': ['yo bebo', 'bebo agua'],
        'madrugo': ['yo madrugo', 'siempre madrugo'],
        'despertarse': ['al despertarse', 'voy a despertarse'],
        'ducharse': ['al ducharse', 'voy a ducharse'],
        'vestirse': ['al vestirse', 'voy a vestirse'],
        'trabajo': ['mi trabajo', 'voy al trabajo'],
        'estudio': ['mi estudio', 'yo estudio'],
        'ordeno': ['yo ordeno', 'ordeno todo'],
        'escucho': ['yo escucho', 'escucho música'],
        'ceno': ['yo ceno', 'ceno tarde'],
        'merienda': ['la merienda', 'para la merienda'],
        'corro': ['yo corro', 'corro rápido'],
        'arreglo': ['yo arreglo', 'arreglo todo'],
        'platico': ['yo platico', 'platico contigo'],

        # Pack 28: City Places
        'ciudad': ['la ciudad', 'en la ciudad'],
        'pueblo': ['el pueblo', 'mi pueblo'],
        'calle': ['la calle', 'en la calle'],
        'plaza': ['la plaza', 'en la plaza'],
        'parque': ['el parque', 'en el parque'],
        'tienda': ['la tienda', 'en la tienda'],
        'supermercado': ['el supermercado', 'al supermercado'],
        'mercado': ['el mercado', 'al mercado'],
        'restaurante': ['el restaurante', 'al restaurante'],
        'bar': ['el bar', 'en el bar'],
        'banco': ['el banco', 'al banco'],
        'oficina': ['la oficina', 'en la oficina'],
        'hospital': ['el hospital', 'al hospital'],
        'farmacia': ['la farmacia', 'a la farmacia'],
        'escuela': ['la escuela', 'a la escuela'],
        'universidad': ['la universidad', 'a la universidad'],
        'biblioteca': ['la biblioteca', 'a la biblioteca'],
        'museo': ['el museo', 'al museo'],
        'cine': ['el cine', 'al cine'],
        'terminal': ['la terminal', 'a la terminal'],

        # Pack 29: Transportation
        'coche': ['el coche', 'en coche'],
        'autobús': ['el autobús', 'en autobús'],
        'tren': ['el tren', 'en tren'],
        'metro': ['el metro', 'en metro'],
        'avión': ['el avión', 'en avión'],
        'bicicleta': ['la bicicleta', 'en bicicleta'],
        'taxi': ['el taxi', 'en taxi'],
        'barco': ['el barco', 'en barco'],
        'moto': ['la moto', 'en moto'],
        'caminar': ['voy a caminar', 'prefiero caminar'],
        'conducir': ['puedo conducir', 'saber conducir'],
        'tranvía': ['el tranvía', 'en tranvía'],
        'ferry': ['el ferry', 'en ferry'],
        'helicóptero': ['el helicóptero', 'en helicóptero'],
        'patinete': ['el patinete', 'en patinete'],

        # Pack 30: Numbers 21-100
        'veintiún': ['número veintiún', 'tengo veintiún'],
        'veintidós': ['número veintidós', 'tengo veintidós'],
        'veintitrés': ['número veintitrés', 'tengo veintitrés'],
        'veinticuatro': ['número veinticuatro', 'tengo veinticuatro'],
        'veinticinco': ['número veinticinco', 'tengo veinticinco'],
        'veintiséis': ['número veintiséis', 'tengo veintiséis'],
        'veintisiete': ['número veintisiete', 'tengo veintisiete'],
        'veintiocho': ['número veintiocho', 'tengo veintiocho'],
        'veintinueve': ['número veintinueve', 'tengo veintinueve'],
        'treinta': ['número treinta', 'tengo treinta'],
        'cuarenta': ['número cuarenta', 'tengo cuarenta'],
        'cincuenta': ['número cincuenta', 'tengo cincuenta'],
        'sesenta': ['número sesenta', 'tengo sesenta'],
        'setenta': ['número setenta', 'tengo setenta'],
        'ochenta': ['número ochenta', 'tengo ochenta'],
        'noventa': ['número noventa', 'tengo noventa'],
        'cien': ['número cien', 'tengo cien'],

        # Pack 31: Gustar (liking)
        'gustar': ['me puede gustar', 'va a gustar'],
        'encantar': ['me puede encantar', 'va a encantar'],
        'interesar': ['me puede interesar', 'va a interesar'],
        'molestar': ['no quiero molestar', 'va a molestar'],
        'importar': ['no me importar', 'va a importar'],
        'aburrir': ['me puede aburrir', 'va a aburrir'],
        'fascinar': ['me puede fascinar', 'va a fascinar'],
        'preocupar': ['me puede preocupar', 'va a preocupar'],
        'sobrar': ['va a sobrar', 'puede sobrar'],
        'caer bien': ['me puede caer bien', 'va a caer bien'],
        'doler': ['me puede doler', 'va a doler'],
        'bastar': ['puede bastar', 'va a bastar'],

        # Pack 32: Weather
        'tiempo': ['el tiempo', 'hace buen tiempo'],
        'frío': ['hace frío', 'mucho frío'],
        'calor': ['hace calor', 'mucho calor'],
        'sol': ['hace sol', 'hay sol'],
        'viento': ['hace viento', 'hay viento'],
        'lluvia': ['hay lluvia', 'la lluvia'],
        'nieve': ['hay nieve', 'la nieve'],
        'nube': ['hay nube', 'la nube'],
        'niebla': ['hay niebla', 'la niebla'],
        'tormenta': ['hay tormenta', 'la tormenta'],
        'clima': ['el clima', 'buen clima'],
        'temperatura': ['la temperatura', 'alta temperatura'],
        'pronóstico': ['el pronóstico', 'buen pronóstico'],
        'húmedo': ['muy húmedo', 'está húmedo'],

        # Pack 33: Poder (can/able)
        'puedo': ['yo puedo', 'puedo hacerlo'],
        'puedes': ['tú puedes', 'puedes hacerlo'],
        'puede': ['él puede', 'puede hacerlo'],
        'podemos': ['nosotros podemos', 'podemos hacerlo'],
        'podéis': ['vosotros podéis', 'podéis hacerlo'],
        'pueden': ['ellos pueden', 'pueden hacerlo'],
        'poder': ['voy a poder', 'quiero poder'],
        'posible': ['es posible', 'si es posible'],
        'imposible': ['es imposible', 'parece imposible'],
        'capaz': ['soy capaz', 'es capaz'],

        # Pack 34: Querer (want)
        'quiero': ['yo quiero', 'quiero ir'],
        'quieres': ['tú quieres', 'quieres ir'],
        'quiere': ['él quiere', 'quiere ir'],
        'queremos': ['nosotros queremos', 'queremos ir'],
        'queréis': ['vosotros queréis', 'queréis ir'],
        'quieren': ['ellos quieren', 'quieren ir'],
        'querer': ['voy a querer', 'puedo querer'],
        'deseo': ['mi deseo', 'tu deseo'],
        'desear': ['puedo desear', 'voy a desear'],
        'ansias': ['con ansias', 'muchas ansias'],

        # Pack 35: School Supplies
        'libro': ['el libro', 'mi libro'],
        'cuaderno': ['el cuaderno', 'mi cuaderno'],
        'lápiz': ['el lápiz', 'mi lápiz'],
        'bolígrafo': ['el bolígrafo', 'mi bolígrafo'],
        'pluma': ['la pluma', 'mi pluma'],
        'papel': ['el papel', 'mi papel'],
        'mochila': ['la mochila', 'mi mochila'],
        'mesa': ['la mesa', 'mi mesa'],
        'silla': ['la silla', 'mi silla'],
        'pizarra': ['la pizarra', 'la pizarra grande'],
        'ordenador': ['el ordenador', 'mi ordenador'],
        'computadora': ['la computadora', 'mi computadora'],
        'estudiante': ['el estudiante', 'soy estudiante'],
        'profesor': ['el profesor', 'mi profesor'],
        'profesora': ['la profesora', 'mi profesora'],
        'clase': ['la clase', 'mi clase'],
        'examen': ['el examen', 'mi examen'],
        'lección': ['la lección', 'mi lección'],
        'aula': ['el aula', 'mi aula'],
        'regla': ['la regla', 'mi regla'],

        # Pack 36: Office & Work
        'jefe': ['el jefe', 'mi jefe'],
        'jefa': ['la jefa', 'mi jefa'],
        'empleado': ['el empleado', 'soy empleado'],
        'empleada': ['la empleada', 'soy empleada'],
        'compañero': ['mi compañero', 'el compañero'],
        'compañera': ['mi compañera', 'la compañera'],
        'cliente': ['el cliente', 'un cliente'],
        'clienta': ['la clienta', 'una clienta'],
        'reunión': ['la reunión', 'en la reunión'],
        'proyecto': ['el proyecto', 'mi proyecto'],
        'documento': ['el documento', 'mi documento'],
        'correo': ['el correo', 'mi correo'],
        'teléfono': ['el teléfono', 'mi teléfono'],
        'salario': ['el salario', 'mi salario'],
        'contrato': ['el contrato', 'mi contrato'],
        'empresa': ['la empresa', 'mi empresa'],
        'negocio': ['el negocio', 'mi negocio'],
        'cita': ['la cita', 'mi cita'],
        'despacho': ['el despacho', 'mi despacho'],
        'cubículo': ['el cubículo', 'mi cubículo'],

        # Pack 37: Animals
        'perro': ['el perro', 'mi perro'],
        'gato': ['el gato', 'mi gato'],
        'pájaro': ['el pájaro', 'un pájaro'],
        'pez': ['el pez', 'un pez'],
        'caballo': ['el caballo', 'un caballo'],
        'vaca': ['la vaca', 'una vaca'],
        'cerdo': ['el cerdo', 'un cerdo'],
        'oveja': ['la oveja', 'una oveja'],
        'ratón': ['el ratón', 'un ratón'],
        'conejo': ['el conejo', 'un conejo'],
        'león': ['el león', 'un león'],
        'tigre': ['el tigre', 'un tigre'],
        'elefante': ['el elefante', 'un elefante'],
        'mono': ['el mono', 'un mono'],
        'serpiente': ['la serpiente', 'una serpiente'],
        'oso': ['el oso', 'un oso'],
        'lobo': ['el lobo', 'un lobo'],
        'mariposa': ['la mariposa', 'una mariposa'],
        'abeja': ['la abeja', 'una abeja'],
        'pato': ['el pato', 'un pato'],

        # Pack 38: Pensar (thinking)
        'pienso': ['yo pienso', 'pienso que sí'],
        'piensas': ['tú piensas', 'qué piensas'],
        'piensa': ['él piensa', 'ella piensa'],
        'pensamos': ['nosotros pensamos', 'pensamos igual'],
        'pensáis': ['vosotros pensáis', 'qué pensáis'],
        'piensan': ['ellos piensan', 'qué piensan'],
        'pensar': ['voy a pensar', 'debo pensar'],
        'pensamiento': ['mi pensamiento', 'el pensamiento'],
        'idea': ['buena idea', 'una idea'],
        'opinión': ['mi opinión', 'tu opinión'],

        # Pack 39: Sentir (feeling)
        'siento': ['lo siento', 'me siento bien'],
        'sientes': ['cómo te sientes', 'qué sientes'],
        'siente': ['cómo se siente', 'él siente'],
        'sentimos': ['lo sentimos', 'nos sentimos'],
        'sentís': ['cómo os sentís', 'qué sentís'],
        'sienten': ['cómo se sienten', 'ellos sienten'],
        'sentir': ['voy a sentir', 'puedo sentir'],
        'sentirse': ['puede sentirse', 'va a sentirse'],
        'sentimiento': ['mi sentimiento', 'el sentimiento'],
        'sensación': ['la sensación', 'buena sensación'],

        # Pack 40: Meals & Food Details
        'desayuno': ['el desayuno', 'para el desayuno'],
        'almuerzo': ['el almuerzo', 'para el almuerzo'],
        'cena': ['la cena', 'para la cena'],
        'sopa': ['la sopa', 'tomar sopa'],
        'bocadillo': ['el bocadillo', 'un bocadillo'],
        'sándwich': ['el sándwich', 'un sándwich'],
        'hamburguesa': ['la hamburguesa', 'una hamburguesa'],
        'pizza': ['la pizza', 'comer pizza'],
        'papas': ['las papas', 'comer papas'],
        'helado': ['el helado', 'un helado'],
        'pastel': ['el pastel', 'un pastel'],
        'torta': ['la torta', 'una torta'],
        'chocolate': ['el chocolate', 'con chocolate'],
        'azúcar': ['el azúcar', 'con azúcar'],
        'sal': ['la sal', 'con sal'],
        'pimienta': ['la pimienta', 'con pimienta'],
        'aceite': ['el aceite', 'con aceite'],
        'vinagre': ['el vinagre', 'con vinagre'],
        'mantequilla': ['la mantequilla', 'con mantequilla'],
        'jamón': ['el jamón', 'con jamón'],
    }

    # If word is in dictionary, return those examples
    if word_lower in examples:
        return examples[word_lower]

    # Otherwise generate generic examples based on patterns
    return generate_generic_examples(word, pack_title)

def generate_generic_examples(word, pack_title):
    """Generate generic examples for words not in the dictionary."""

    word_lower = word.lower()

    # Check for verb conjugation patterns (first person -o ending)
    if word_lower.endswith('o') and len(word_lower) > 2:
        return [f'yo {word}', f'{word} bien']

    # Check for verb conjugation patterns (-es, -as endings)
    if word_lower.endswith(('es', 'as')) and len(word_lower) > 3:
        return [f'tú {word}', f'{word} bien']

    # Check for verb conjugation patterns (-e, -a endings for él/ella)
    if word_lower.endswith(('e', 'a')) and len(word_lower) > 3:
        if 'él' in pack_title or 'ella' in pack_title or any(x in pack_title.lower() for x in ['verb', 'ing', 'ar', 'er', 'ir']):
            return [f'él {word}', f'ella {word}']

    # Check for infinitive verbs (-ar, -er, -ir endings)
    if word_lower.endswith(('ar', 'er', 'ir')) and len(word_lower) > 3:
        return [f'voy a {word}', f'puedo {word}']

    # Check for adjectives (commonly end in -o, -a, -e, -oso, -ivo)
    if word_lower.endswith(('oso', 'ivo', 'ado', 'ido')):
        return [f'muy {word}', f'es {word}']

    # Check for nouns with articles
    if pack_title.lower() in ['animals', 'food', 'places', 'clothing', 'body parts', 'furniture', 'tools']:
        return [f'el {word}', f'un {word}']

    # Default: use with common phrases
    return [f'el {word}', f'mi {word}']

def process_csv():
    """Process the CSV and add example words."""

    csv_path = '/home/user/LPH/SpanishWords/SpanishWordsOverview.csv'
    output_path = '/home/user/LPH/SpanishWords/SpanishWordsOverview_with_examples.csv'

    rows = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pack_num = row['Pack_Number']
            pack_title = row['Pack_Title']
            base_words_str = row['Spanish_Base_Words']

            # Parse base words
            words_content = base_words_str.strip()[1:-1]
            base_words = [w.strip() for w in words_content.split(',')]

            # Generate examples for each base word
            example_words = []
            for base_word in base_words:
                examples = generate_examples(base_word, pack_title)
                example_words.extend(examples)

            # Create combined words
            combined_words = base_words + example_words

            # Add to row
            row['Spanish_Example_Words'] = format_word_list(example_words)
            row['Spanish_Combined_Words'] = format_word_list(combined_words)

            rows.append(row)

    # Write output
    fieldnames = ['Pack_Number', 'Pack_Title', 'Difficulty_Act', 'Spanish_Base_Words', 'Spanish_Example_Words', 'Spanish_Combined_Words']

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Output written to: {output_path}")
    print(f"Total packs processed: {len(rows)}")

    # Show sample
    print("\nSample output (Pack 1):")
    sample = rows[0]
    print(f"Base words: {sample['Spanish_Base_Words'][:100]}...")
    print(f"Example words: {sample['Spanish_Example_Words'][:100]}...")

if __name__ == '__main__':
    process_csv()

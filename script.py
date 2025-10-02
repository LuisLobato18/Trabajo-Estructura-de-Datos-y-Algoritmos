from datetime import datetime
import csv
import queue

class ListaProyectos:
    def __init__(self):
        self.elementos = []
        self.tamaño = 0

    def agregar_proyecto(self, proyecto):
        self.elementos.append(proyecto)
        self.tamaño += 1

    def buscar_proyecto(self, criterio, valor):
        resultados = []
        for elemento in self.elementos:
            if criterio == 'id' and elemento[0] == valor:
                resultados.append(elemento)
            elif criterio == 'nombre' and elemento[1].lower() == valor.lower():
                resultados.append(elemento)
            elif criterio == 'cliente' and elemento[2].lower() == valor.lower():
                resultados.append(elemento)
        return resultados

    def listar_todos(self):
        return self.elementos.copy()

    def ordenar_por_nombre(self):
        n = len(self.elementos)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.elementos[j][1] > self.elementos[j + 1][1]:
                    self.elementos[j], self.elementos[j + 1] = self.elementos[j + 1], self.elementos[j]

    def eliminar_proyecto(self, proyecto_id):
        for i, elemento in enumerate(self.elementos):
            if elemento[0] == proyecto_id:
                eliminado = self.elementos.pop(i)
                self.tamaño -= 1
                return eliminado
        return None

class ColaTareas:
    def __init__(self):
        self.cola = queue.Queue()
        self.elementos = []
        self.contador_id = 1

    def encolar(self, tarea):
        tarea[0] = self.contador_id
        self.cola.put(tarea)
        self.elementos.append(tarea.copy())
        self.contador_id += 1

    def desencolar(self):
        if self.esta_vacia():
            return None
        tarea = self.cola.get()
        for i, elemento in enumerate(self.elementos):
            if elemento[0] == tarea[0]:
                self.elementos.pop(i)
                break
        return tarea

    def ver_primera_tarea(self):
        if self.esta_vacia():
            return None
        if len(self.elementos) > 0:
            return self.elementos[0]
        return None

    def esta_vacia(self):
        return self.cola.empty()

    def tamaño(self):
        return self.cola.qsize()

    def buscar_tarea_por_desarrollador(self, desarrollador):
        resultados = []
        for tarea in self.elementos:
            if tarea[3].lower() == desarrollador.lower():
                resultados.append(tarea)
        return resultados

class PilaCambios:
    def __init__(self):
        self.pila = queue.LifoQueue()
        self.elementos = []
        self.contador_id = 1

    def apilar(self, cambio):
        cambio[0] = self.contador_id
        self.pila.put(cambio)
        self.elementos.append(cambio.copy())
        self.contador_id += 1

    def desapilar(self):
        if self.esta_vacia():
            return None
        cambio = self.pila.get()
        for i in range(len(self.elementos) - 1, -1, -1):
            if self.elementos[i][0] == cambio[0]:
                self.elementos.pop(i)
                break
        return cambio

    def ver_ultimo_cambio_sin_remover(self):
        if self.esta_vacia():
            return None
        if len(self.elementos) > 0:
            return self.elementos[-1]
        return None

    def esta_vacia(self):
        return self.pila.empty()

    def tamaño(self):
        return self.pila.qsize()

    def obtener_cambios_proyecto(self, proyecto_id):
        cambios_proyecto = []
        for cambio in self.elementos:
            if cambio[1] == proyecto_id:
                cambios_proyecto.append(cambio)
        return cambios_proyecto

class HistorialVersiones:
    def __init__(self):
        self.elementos = []
        self.tamaño = 0

    def agregar_version(self, version):
        self.elementos.append(version)
        self.tamaño += 1

    def buscar_version(self, criterio, valor):
        resultados = []
        for elemento in self.elementos:
            if criterio == 'autor' and elemento[2].lower() == valor.lower():
                resultados.append(elemento)
            elif criterio == 'funcion' and elemento[3].lower() == valor.lower():
                resultados.append(elemento)
            elif criterio == 'proyecto_id' and elemento[1] == valor:
                resultados.append(elemento)
        return resultados

    def listar_todos(self):
        return self.elementos.copy()

    def obtener_ultima_version_proyecto(self, proyecto_id):
        versiones_proyecto = self.buscar_version('proyecto_id', proyecto_id)
        if versiones_proyecto:
            return versiones_proyecto[-1]
        else:
            return None

class SistemaGestionVersiones:
    def __init__(self):
        self.lista_proyectos = ListaProyectos()
        self.cola_tareas = ColaTareas()
        self.pila_cambios = PilaCambios()
        self.historial_versiones = HistorialVersiones()

        self.ids_proyectos = []
        self.valores_ganados = []
        self.costos_reales = []
        self.valores_planeados = []
        self.cpis = []
        self.spis = []

        self.desarrolladores = []
        self.tareas_completadas_dev = []
        self.tareas_pendientes_dev = []

        self.contador_ids = 1

    def validar_fecha(self, fecha):
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            return True
        except ValueError:
            print("Formato de fecha incorrecto. Use DD/MM/YYYY")
            return False

    def validar_numero(self, valor, mensaje=" Debe ser un número válido"):
        try:
            return float(valor)
        except ValueError:
            print(mensaje)
            return None

    def buscar_proyecto_por_id(self, proyecto_id):
        proyectos = self.lista_proyectos.buscar_proyecto('id', proyecto_id)
        if proyectos:
            return proyectos[0]
        else:
            return None

    def buscar_indice_indicador(self, proyecto_id):
        try:
            return self.ids_proyectos.index(proyecto_id)
        except ValueError:
            return -1

    def buscar_indice_desarrollador(self, desarrollador):
        try:
            return self.desarrolladores.index(desarrollador.lower())
        except ValueError:
            return -1

    def agregar_desarrollador(self, desarrollador):
        if self.buscar_indice_desarrollador(desarrollador) == -1:
            self.desarrolladores.append(desarrollador.lower())
            self.tareas_completadas_dev.append(0)
            self.tareas_pendientes_dev.append(0)

    def mostrar_menu_principal(self):
        print("\n" + "=" * 70)
        print("   SISTEMA DE GESTIÓN DE VERSIONES Y CONTROL DE CAMBIOS")
        print("                    MSS SEIDOR PERU")
        print("=" * 70)
        print("1. Gestión de Proyectos")
        print("2. Gestión de Tareas")
        print("3. Gestión de Cambios")
        print("4. Gestión de Versiones")
        print("5. Indicadores y Reportes")
        print("6. Estadísticas por Desarrollador")
        print("0. Salir del sistema")
        print("=" * 70)

    def mostrar_menu_proyectos(self):
        print("\n--- GESTIÓN DE PROYECTOS ---")
        print("1. Registrar nuevo proyecto")
        print("2. Listar todos los proyectos")
        print("3. Buscar proyecto")
        print("4. Ordenar proyectos por nombre")
        print("5. Eliminar proyecto")
        print("0. Volver al menú principal")

    def mostrar_menu_tareas(self):
        print("\n--- GESTIÓN DE TAREAS ---")
        print("1. Asignar nueva tarea")
        print("2. Ver cola de tareas pendientes")
        print("3. Completar primera tarea")
        print("4. Buscar tareas por desarrollador")
        print("0. Volver al menú principal")

    def mostrar_menu_cambios(self):
        print("\n--- GESTIÓN DE CAMBIOS ---")
        print("1. Registrar nuevo cambio")
        print("2. Ver último cambio")
        print("3. Deshacer último cambio")
        print("4. Ver historial de cambios por proyecto")
        print("0. Volver al menú principal")

    def mostrar_menu_versiones(self):
        print("\n--- GESTIÓN DE VERSIONES ---")
        print("1. Agregar nueva versión")
        print("2. Buscar versión por autor")
        print("3. Buscar versión por función")
        print("4. Ver versiones de un proyecto")
        print("5. Ver última versión de un proyecto")
        print("0. Volver al menú principal")

    def registrar_proyecto(self):
        print("\n--- REGISTRAR NUEVO PROYECTO ---")
        nombre = input("Nombre del proyecto: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío")
            return

        cliente = input("Cliente: ").strip()
        fecha_inicio = input("Fecha de inicio (DD/MM/YYYY): ")

        if not self.validar_fecha(fecha_inicio):
            return

        presupuesto_input = input("Presupuesto estimado: ")
        presupuesto = self.validar_numero(presupuesto_input)
        if presupuesto is None:
            return

        proyecto = [
            self.contador_ids,
            nombre,
            cliente,
            fecha_inicio,
            presupuesto,
            'Activo',
            datetime.now().strftime("%d/%m/%Y %H:%M")
        ]

        self.lista_proyectos.agregar_proyecto(proyecto)

        self.ids_proyectos.append(self.contador_ids)
        self.valores_ganados.append(0)
        self.costos_reales.append(0)
        self.valores_planeados.append(presupuesto)
        self.cpis.append(0)
        self.spis.append(0)

        print(f"Proyecto '{nombre}' registrado con ID: {self.contador_ids}")
        self.contador_ids += 1

    def listar_proyectos(self):
        print("\n--- LISTA DE PROYECTOS ---")
        proyectos = self.lista_proyectos.listar_todos()

        if not proyectos:
            print(" No hay proyectos registrados")
            return

        print(f"Total de proyectos: {len(proyectos)}")
        print("-" * 80)
        for proyecto in proyectos:
            print(f"ID: {proyecto[0]} | {proyecto[1]} | Cliente: {proyecto[2]}")
            print(f"Inicio: {proyecto[3]} | Presupuesto: ${proyecto[4]:,.2f} | Estado: {proyecto[5]}")
            print("-" * 80)

    def buscar_proyecto(self):
        print("\n--- BUSCAR PROYECTO ---")
        print("1. Buscar por ID")
        print("2. Buscar por nombre")
        print("3. Buscar por cliente")

        opcion = input("Seleccione criterio: ")

        if opcion == "1":
            try:
                proyecto_id = int(input("ID del proyecto: "))
                resultados = self.lista_proyectos.buscar_proyecto('id', proyecto_id)
                criterio = "ID"
            except ValueError:
                print(" ID debe ser un número")
                return
        elif opcion == "2":
            nombre = input("Nombre del proyecto: ")
            resultados = self.lista_proyectos.buscar_proyecto('nombre', nombre)
            criterio = "nombre"
        elif opcion == "3":
            cliente = input("Cliente: ")
            resultados = self.lista_proyectos.buscar_proyecto('cliente', cliente)
            criterio = "cliente"
        else:
            print(" Opción inválida")
            return

        if resultados:
            print(f"\n Encontrados {len(resultados)} proyecto(s) por {criterio}:")
            for proyecto in resultados:
                print(f"  ID: {proyecto[0]} - {proyecto[1]} ({proyecto[2]})")
        else:
            print(f" No se encontraron proyectos con ese {criterio}")

    def asignar_tarea(self):
        print("\n--- ASIGNAR NUEVA TAREA ---")
        self.listar_proyectos()

        try:
            proyecto_id = int(input("ID del proyecto: "))
            if not self.buscar_proyecto_por_id(proyecto_id):
                print(" Proyecto no encontrado")
                return

            descripcion = input("Descripción de la tarea: ").strip()
            desarrollador = input("Desarrollador responsable: ").strip()
            prioridad = input("Prioridad (Alta/Media/Baja): ").strip()
            fecha_limite = input("Fecha límite (DD/MM/YYYY): ")

            if not self.validar_fecha(fecha_limite):
                return

            tarea = [
                0,
                proyecto_id,
                descripcion,
                desarrollador,
                prioridad,
                fecha_limite,
                'Pendiente',
                datetime.now().strftime("%d/%m/%Y %H:%M")
            ]

            self.cola_tareas.encolar(tarea)
            self.agregar_desarrollador(desarrollador)

            indice_dev = self.buscar_indice_desarrollador(desarrollador)
            if indice_dev >= 0:
                self.tareas_pendientes_dev[indice_dev] += 1

            print(f" Tarea asignada a {desarrollador}")

        except ValueError:
            print(" ID del proyecto debe ser un número")

    def ver_cola_tareas(self):
        print("\n--- COLA DE TAREAS PENDIENTES ---")

        if self.cola_tareas.esta_vacia():
            print("No hay tareas pendientes")
            return

        print(f"Total de tareas en cola: {self.cola_tareas.tamaño()}")
        print("\nPróxima tarea a procesar:")
        primera_tarea = self.cola_tareas.ver_primera_tarea()
        if primera_tarea:
            proyecto = self.buscar_proyecto_por_id(primera_tarea[1])
            if proyecto:
                proyecto_nombre = proyecto[1]
            else:
                proyecto_nombre = "Desconocido"

            print(f"   {primera_tarea[2]}")
            print(f"   Proyecto: {proyecto_nombre}")
            print(f"   Desarrollador: {primera_tarea[3]}")
            print(f"   Prioridad: {primera_tarea[4]}")
            print(f"   Límite: {primera_tarea[5]}")

        print(f"\nTodas las tareas en cola:")
        for i, tarea in enumerate(self.cola_tareas.elementos):
            proyecto = self.buscar_proyecto_por_id(tarea[1])
            if proyecto:
                proyecto_nombre = proyecto[1]
            else:
                proyecto_nombre = "Desconocido"
            print(f"  {i + 1}. {tarea[2]} - {tarea[3]} ({proyecto_nombre})")

    def completar_primera_tarea(self):
        print("\n--- COMPLETAR PRIMERA TAREA ---")

        if self.cola_tareas.esta_vacia():
            print("No hay tareas para completar")
            return

        tarea = self.cola_tareas.desencolar()
        if tarea:
            if len(tarea) > 6:
                tarea[6] = 'Completada'
            else:
                tarea.append('Completada')
            fecha_completado = datetime.now().strftime("%d/%m/%Y %H:%M")
            tarea.append(fecha_completado)

            indice_dev = self.buscar_indice_desarrollador(tarea[3])
            if indice_dev >= 0:
                self.tareas_completadas_dev[indice_dev] += 1
                if self.tareas_pendientes_dev[indice_dev] > 0:
                    self.tareas_pendientes_dev[indice_dev] -= 1

            print(f"Tarea completada:")
            print(f"   {tarea[2]}")
            print(f"   {tarea[3]}")
            print(f"   Completada: {fecha_completado}")
            print(f"   Tareas restantes: {self.cola_tareas.tamaño()}")

    def registrar_cambio(self):
        print("\n--- REGISTRAR NUEVO CAMBIO ---")
        self.listar_proyectos()

        try:
            proyecto_id = int(input("ID del proyecto: "))
            if not self.buscar_proyecto_por_id(proyecto_id):
                print(" Proyecto no encontrado")
                return

            tipo_cambio = input("Tipo de cambio (Bugfix/Feature/Refactor): ").strip()
            descripcion = input("Descripción del cambio: ").strip()
            autor = input("Autor del cambio: ").strip()

            cambio = [
                0,
                proyecto_id,
                tipo_cambio,
                descripcion,
                autor,
                datetime.now().strftime("%d/%m/%Y %H:%M")
            ]

            self.pila_cambios.apilar(cambio)
            print(f"Cambio registrado (#{self.pila_cambios.contador_id - 1})")

        except ValueError:
            print(" ID del proyecto debe ser un número")

    def ver_ultimo_cambio(self):
        print("\n--- ÚLTIMO CAMBIO REGISTRADO ---")

        ultimo = self.pila_cambios.ver_ultimo_cambio_sin_remover()
        if ultimo:
            proyecto = self.buscar_proyecto_por_id(ultimo[1])
            if proyecto:
                proyecto_nombre = proyecto[1]
            else:
                proyecto_nombre = "Desconocido"

            print(f" Cambio #{ultimo[0]}")
            print(f" Proyecto: {proyecto_nombre}")
            print(f" Tipo: {ultimo[2]}")
            print(f" Descripción: {ultimo[3]}")
            print(f" Autor: {ultimo[4]}")
            print(f" Fecha: {ultimo[5]}")
        else:
            print("No hay cambios registrados")

    def deshacer_ultimo_cambio(self):
        print("\n--- DESHACER ÚLTIMO CAMBIO ---")

        if self.pila_cambios.esta_vacia():
            print("No hay cambios para deshacer")
            return

        ultimo_cambio = self.pila_cambios.desapilar()
        print(f"️  Cambio deshecho:")
        print(f"  {ultimo_cambio[3]}")
        print(f"  {ultimo_cambio[4]}")
        print(f"  {ultimo_cambio[5]}")
        print(f"  Cambios restantes en pila: {self.pila_cambios.tamaño()}")

    def agregar_version(self):
        print("\n--- AGREGAR NUEVA VERSIÓN ---")
        self.listar_proyectos()

        try:
            proyecto_id = int(input("ID del proyecto: "))
            if not self.buscar_proyecto_por_id(proyecto_id):
                print("Proyecto no encontrado")
                return

            autor = input("Autor de la versión: ").strip()
            funcion = input("Función desarrollada: ").strip()
            descripcion = input("Descripción de la versión: ").strip()

            version = [
                self.historial_versiones.tamaño + 1,
                proyecto_id,
                autor,
                funcion,
                descripcion,
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                'Activa'
            ]

            self.historial_versiones.agregar_version(version)
            print(f" Versión agregada (#{version[0]})")

        except ValueError:
            print(" ID del proyecto debe ser un número")

    def buscar_version_por_autor(self):
        print("\n--- BUSCAR VERSIÓN POR AUTOR ---")
        autor = input("Nombre del autor: ").strip()

        resultados = self.historial_versiones.buscar_version('autor', autor)
        if resultados:
            print(f" Encontradas {len(resultados)} versión(es) de {autor}:")
            for version in resultados:
                proyecto = self.buscar_proyecto_por_id(version[1])
                if proyecto:
                    proyecto_nombre = proyecto[1]
                else:
                    proyecto_nombre = "Desconocido"
                print(f" V{version[0]} - {proyecto_nombre}")
                print(f"  {version[3]} - {version[4]}")
                print(f"  {version[5]}")
        else:
            print(f" No se encontraron versiones de {autor}")

    def calcular_indicadores_cpi_spi(self):
        print("\n--- CALCULAR INDICADORES CPI/SPI ---")
        self.listar_proyectos()

        try:
            proyecto_id = int(input("ID del proyecto: "))
            indice = self.buscar_indice_indicador(proyecto_id)

            if indice == -1:
                print(" Proyecto no encontrado")
                return

            valor_ganado = self.validar_numero(input("Valor ganado actual: "))
            if valor_ganado is None:
                return

            costo_real = self.validar_numero(input("Costo real actual: "))
            if costo_real is None:
                return

            self.valores_ganados[indice] = valor_ganado
            self.costos_reales[indice] = costo_real

            if costo_real > 0:
                self.cpis[indice] = valor_ganado / costo_real
            else:
                self.cpis[indice] = 0

            if self.valores_planeados[indice] > 0:
                self.spis[indice] = valor_ganado / self.valores_planeados[indice]
            else:
                self.spis[indice] = 0

            cpi = self.cpis[indice]
            spi = self.spis[indice]

            print(f"\n📊 INDICADORES DE RENDIMIENTO:")
            print(f"  CPI: {cpi:.2f}")
            print(f"  SPI: {spi:.2f}")

        except ValueError:
            print(" ID debe ser un número")

    def mostrar_estadisticas_desarrolladores(self):
        print("\n--- ESTADÍSTICAS POR DESARROLLADOR ---")

        if not self.desarrolladores:
            print("No hay desarrolladores registrados")
            return

        print(f"Total de desarrolladores: {len(self.desarrolladores)}")
        print("-" * 60)

        for i, dev in enumerate(self.desarrolladores):
            completadas = self.tareas_completadas_dev[i]
            pendientes = self.tareas_pendientes_dev[i]
            total = completadas + pendientes

            print(f" {dev.title()}")
            print(f" Completadas: {completadas}")
            print(f" Pendientes: {pendientes}")
            print(f" Total asignadas: {total}")
            if total > 0:
                eficiencia = (completadas / total) * 100
                print(f" Eficiencia: {eficiencia:.1f}%")
            print("-" * 60)

    def generar_reporte_completo(self):
        print("\n---  REPORTE COMPLETO DEL SISTEMA ---")

        total_proyectos = self.lista_proyectos.tamaño
        total_tareas = self.cola_tareas.tamaño()
        total_cambios = self.pila_cambios.tamaño()
        total_versiones = self.historial_versiones.tamaño

        print(f" RESUMEN EJECUTIVO:")
        print(f"   Proyectos activos: {total_proyectos}")
        print(f"   Tareas pendientes: {total_tareas}")
        print(f"   Cambios registrados: {total_cambios}")
        print(f"   Versiones desarrolladas: {total_versiones}")
        print(f"   Desarrolladores activos: {len(self.desarrolladores)}")

        if total_cambios > 0:
            proyectos_con_cambios = []
            cantidad_cambios = []

            for cambio in self.pila_cambios.elementos:
                proyecto_id = cambio[1]

                encontrado = False
                for i in range(len(proyectos_con_cambios)):
                    if proyectos_con_cambios[i] == proyecto_id:
                        cantidad_cambios[i] += 1
                        encontrado = True
                        break

                if not encontrado:
                    proyectos_con_cambios.append(proyecto_id)
                    cantidad_cambios.append(1)

            if len(proyectos_con_cambios) > 0:
                max_cambios = 0
                proyecto_max_cambios = 0
                for i in range(len(cantidad_cambios)):
                    if cantidad_cambios[i] > max_cambios:
                        max_cambios = cantidad_cambios[i]
                        proyecto_max_cambios = proyectos_con_cambios[i]

                proyecto = self.buscar_proyecto_por_id(proyecto_max_cambios)
                if proyecto:
                    print(f"\nProyecto con más actividad: {proyecto[1]} ({max_cambios} cambios)")

        print(f"\n ESTADO DE ESTRUCTURAS:")
        print(f"   Lista de proyectos: {self.lista_proyectos.tamaño} elementos")
        print(f"   Cola de tareas: {self.cola_tareas.tamaño()} elementos")
        print(f"   Pila de cambios: {self.pila_cambios.tamaño()} elementos")
        print(f"   Historial versiones: {self.historial_versiones.tamaño} elementos")

    def ejecutar_gestion_proyectos(self):
        while True:
            self.mostrar_menu_proyectos()
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.registrar_proyecto()
            elif opcion == "2":
                self.listar_proyectos()
            elif opcion == "3":
                self.buscar_proyecto()
            elif opcion == "4":
                self.lista_proyectos.ordenar_por_nombre()
                print("Proyectos ordenados por nombre")
                self.listar_proyectos()
            elif opcion == "5":
                try:
                    proyecto_id = int(input("ID del proyecto a eliminar: "))
                    eliminado = self.lista_proyectos.eliminar_proyecto(proyecto_id)
                    if eliminado:
                        print(f"Proyecto '{eliminado[1]}' eliminado")
                    else:
                        print("Proyecto no encontrado")
                except ValueError:
                    print("ID debe ser un número")
            elif opcion == "0":
                break
            else:
                print("Opción inválida")

            input("\nPresione Enter para continuar...")

    def ejecutar_gestion_tareas(self):
        while True:
            self.mostrar_menu_tareas()
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.asignar_tarea()
            elif opcion == "2":
                self.ver_cola_tareas()
            elif opcion == "3":
                self.completar_primera_tarea()
            elif opcion == "4":
                desarrollador = input("Nombre del desarrollador: ")
                tareas = self.cola_tareas.buscar_tarea_por_desarrollador(desarrollador)
                if tareas:
                    print(f"Tareas de {desarrollador}:")
                    for tarea in tareas:
                        print(f"{tarea[2]} - Prioridad: {tarea[4]}")
                else:
                    print(f"No se encontraron tareas para {desarrollador}")
            elif opcion == "0":
                break
            else:
                print(" Opción inválida")

            input("\nPresione Enter para continuar...")

    def ejecutar_gestion_cambios(self):
        while True:
            self.mostrar_menu_cambios()
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.registrar_cambio()
            elif opcion == "2":
                self.ver_ultimo_cambio()
            elif opcion == "3":
                self.deshacer_ultimo_cambio()
            elif opcion == "4":
                try:
                    proyecto_id = int(input("ID del proyecto: "))
                    cambios = self.pila_cambios.obtener_cambios_proyecto(proyecto_id)
                    if cambios:
                        print(f"Cambios del proyecto {proyecto_id}:")
                        for cambio in reversed(cambios):
                            print(f" {cambio[2]}: {cambio[3]} ({cambio[4]})")
                    else:
                        print(f"No hay cambios para el proyecto {proyecto_id}")
                except ValueError:
                    print("ID debe ser un número")
            elif opcion == "0":
                break
            else:
                print(" Opción inválida")

            input("\nPresione Enter para continuar...")

    def ejecutar_gestion_versiones(self):
        while True:
            self.mostrar_menu_versiones()
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.agregar_version()
            elif opcion == "2":
                self.buscar_version_por_autor()
            elif opcion == "3":
                funcion = input("Función a buscar: ").strip()
                resultados = self.historial_versiones.buscar_version('funcion', funcion)
                if resultados:
                    print(f"Encontradas {len(resultados)} versión(es) con función '{funcion}':")
                    for version in resultados:
                        print(f"   V{version[0]} por {version[2]} - {version[4]}")
                else:
                    print(f"No se encontraron versiones con función '{funcion}'")
            elif opcion == "4":
                try:
                    proyecto_id = int(input("ID del proyecto: "))
                    versiones = self.historial_versiones.buscar_version('proyecto_id', proyecto_id)
                    if versiones:
                        print(f"Versiones del proyecto {proyecto_id}:")
                        for version in versiones:
                            print(f"   V{version[0]} - {version[3]} por {version[2]} ({version[5]})")
                    else:
                        print(f"No hay versiones para el proyecto {proyecto_id}")
                except ValueError:
                    print("ID debe ser un número")
            elif opcion == "5":
                try:
                    proyecto_id = int(input("ID del proyecto: "))
                    ultima_version = self.historial_versiones.obtener_ultima_version_proyecto(proyecto_id)
                    if ultima_version:
                        print(f" Última versión del proyecto {proyecto_id}:")
                        print(f"   V{ultima_version[0]} - {ultima_version[3]}")
                        print(f"   Autor: {ultima_version[2]}")
                        print(f"   Descripción: {ultima_version[4]}")
                        print(f"   Fecha: {ultima_version[5]}")
                    else:
                        print(f"No hay versiones para el proyecto {proyecto_id}")
                except ValueError:
                    print("ID debe ser un número")
            elif opcion == "0":
                break
            else:
                print("Opción inválida")

            input("\nPresione Enter para continuar...")

    def mostrar_menu_indicadores(self):
        print("\n--- INDICADORES Y REPORTES ---")
        print("1. Calcular indicadores CPI/SPI")
        print("2. Ver reporte completo del sistema")
        print("3. Exportar datos a CSV")
        print("0. Volver al menú principal")

    def ejecutar_indicadores_reportes(self):
        while True:
            self.mostrar_menu_indicadores()
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.calcular_indicadores_cpi_spi()
            elif opcion == "2":
                self.generar_reporte_completo()
            elif opcion == "3":
                self.exportar_datos_csv()
            elif opcion == "0":
                break
            else:
                print("Opción inválida")

            input("\nPresione Enter para continuar...")

    def exportar_datos_csv(self):
        print("\n--- EXPORTAR DATOS A CSV ---")

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivos_generados = []

            nombre_proyectos = f"lista_proyectos_{timestamp}.csv"
            with open(nombre_proyectos, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow(['ID', 'Nombre', 'Cliente', 'Fecha_Inicio', 'Presupuesto', 'Estado', 'Fecha_Registro'])

                for proyecto in self.lista_proyectos.elementos:
                    writer.writerow(proyecto)
            archivos_generados.append(nombre_proyectos)

            nombre_tareas = f"cola_tareas_{timestamp}.csv"
            with open(nombre_tareas, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow(
                    ['ID', 'Proyecto_ID', 'Descripcion', 'Desarrollador', 'Prioridad', 'Fecha_Limite', 'Estado',
                     'Fecha_Asignacion'])

                for tarea in self.cola_tareas.elementos:
                    writer.writerow(tarea)
            archivos_generados.append(nombre_tareas)

            nombre_cambios = f"pila_cambios_{timestamp}.csv"
            with open(nombre_cambios, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow(['ID', 'Proyecto_ID', 'Tipo', 'Descripcion', 'Autor', 'Fecha'])

                for cambio in self.pila_cambios.elementos:
                    writer.writerow(cambio)
            archivos_generados.append(nombre_cambios)

            nombre_versiones = f"lista_versiones_{timestamp}.csv"
            with open(nombre_versiones, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow(['ID', 'Proyecto_ID', 'Autor', 'Funcion', 'Descripcion', 'Fecha', 'Estado'])

                for version in self.historial_versiones.elementos:
                    writer.writerow(version)
            archivos_generados.append(nombre_versiones)

            nombre_indicadores = f"arrays_indicadores_{timestamp}.csv"
            with open(nombre_indicadores, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow(['Proyecto_ID', 'Valor_Ganado', 'Costo_Real', 'Valor_Planeado', 'CPI', 'SPI'])

                for i in range(len(self.ids_proyectos)):
                    writer.writerow([
                        self.ids_proyectos[i],
                        self.valores_ganados[i],
                        self.costos_reales[i],
                        self.valores_planeados[i],
                        round(self.cpis[i], 2),
                        round(self.spis[i], 2)
                    ])
            archivos_generados.append(nombre_indicadores)

            nombre_desarrolladores = f"arrays_desarrolladores_{timestamp}.csv"
            with open(nombre_desarrolladores, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow(['Desarrollador', 'Tareas_Completadas', 'Tareas_Pendientes', 'Total_Asignadas',
                                 'Eficiencia_Porcentaje'])

                for i in range(len(self.desarrolladores)):
                    completadas = self.tareas_completadas_dev[i]
                    pendientes = self.tareas_pendientes_dev[i]
                    total = completadas + pendientes
                    eficiencia = (completadas / total * 100) if total > 0 else 0

                    writer.writerow([
                        self.desarrolladores[i].title(),
                        completadas,
                        pendientes,
                        total,
                        round(eficiencia, 1)
                    ])
            archivos_generados.append(nombre_desarrolladores)

            print(f"Exportación completada:")
            print(f"Archivos generados: {len(archivos_generados)}")
            for archivo in archivos_generados:
                print(f"   • {archivo}")

        except Exception as e:
            print(f" Error durante la exportación: {e}")

    def ejecutar_sistema(self):
        print("Iniciando Sistema de Gestión de Versiones y Control de Cambios")
        print("MSS SEIDOR PERU - Estructuras de Datos Optimizadas")

        while True:
            try:
                self.mostrar_menu_principal()
                opcion = input("\nSeleccione una opción: ")

                if opcion == "1":
                    self.ejecutar_gestion_proyectos()
                elif opcion == "2":
                    self.ejecutar_gestion_tareas()
                elif opcion == "3":
                    self.ejecutar_gestion_cambios()
                elif opcion == "4":
                    self.ejecutar_gestion_versiones()
                elif opcion == "5":
                    self.ejecutar_indicadores_reportes()
                elif opcion == "6":
                    self.mostrar_estadisticas_desarrolladores()
                    input("\nPresione Enter para continuar...")
                elif opcion == "0":
                    print("\nGracias por usar el Sistema de Gestión de Versiones")
                    print("Sistema finalizado exitosamente")
                    break
                else:
                    print("Opción inválida. Seleccione una opción del 0 al 6")

            except ValueError as e:
                print(f"Error de entrada: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")

def main():
    sistema = SistemaGestionVersiones()
    sistema.ejecutar_sistema()

if __name__ == "__main__":
    main()

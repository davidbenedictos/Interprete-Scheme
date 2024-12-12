from antlr4 import *
from SchemeLexer import SchemeLexer
from SchemeParser import SchemeParser
from SchemeVisitor import SchemeVisitor

# Visitor para evaluar expresiones de Mini Scheme
class SchemeEvalVisitor(SchemeVisitor):
    def __init__(self):
        self.symbols = {}  # Tabla de símbolos para variables y funciones
    
    def visitRoot(self, ctx):
        results = []
        for expr in ctx.expr():
            result = self.visit(expr)
            results.append(result)
        return results



    def visitDefinicionFuncion(self, ctx):
        # Obtener el nombre de la función
        function_name = ctx.getChild(3).getText()  # IDENT está en el tercer hijo (índice 2)

        # Obtener los parámetros
        parameters = [param.getText() for param in ctx.paramList().IDENT()]

        # Obtener el cuerpo de la función
        body = ctx.expr()  # expr+ devuelve una lista de nodos
       
        # Registrar la función en la tabla de símbolos
        self.symbols[function_name] = {
            "params": parameters,
            "body": body
        }
        

    def visitLiteralLista(self, ctx):
        x = [self.visit(expr) for expr in ctx.expr()]
        return x
    
    def visitOperacionCar(self, ctx):
        name = ctx.IDENT().getText()
        if name in self.symbols:
            lista = self.symbols[name]
            if not isinstance(lista, list): # no es lista
                raise TypeError("Argumento no es una lista")
            if not lista:
                raise ValueError("car no se aplica a listas vacias")
            return lista[0]
        else:
            raise NameError(f"Variable {lista} no definida")
    
    def visitOperacionCdr(self, ctx):
        name = ctx.IDENT().getText()
        if name in self.symbols:
            lista = self.symbols[name]
            if not isinstance(lista, list): # no es lista
                raise TypeError("Argumento no es una lista")
            if not lista:
                raise ValueError("car no se aplica a listas vacias")
            return lista[1:]
        else:
            raise NameError(f"Variable {lista} no definida")
        
    def visitOperacionCons(self, ctx):
        # Evaluar el primer argumento (el valor que será el nuevo "car")
        value = self.visit(ctx.expr(0))

        # Evaluar el segundo argumento (la lista existente que será el "cdr")
        lista = self.visit(ctx.expr(1))

        # Verificar que el segundo argumento sea una lista
        if not isinstance(lista, list):
            raise TypeError("El segundo argumento de 'cons' debe ser una lista")

        # Retornar una nueva lista con 'value' al inicio
        return [value] + lista

    def visitOperacionNull(self, ctx):
        # Evaluar la expresión del argumento
        arg = self.visit(ctx.expr())
        
        # Verificar si el resultado es una lista
        if not isinstance(arg, list):
            raise TypeError("Argumento de 'null?' debe ser una lista")
        
        # Retornar True si la lista está vacía, False en caso contrario
        if len(arg) == 0:
            return True
        return False


        

    def visitDefinicionVariable(self, ctx):
        variable_name = ctx.IDENT().getText()
        value = self.visit(ctx.expr())
        self.symbols[variable_name] = value


    def visitLlamadaFuncion(self, ctx):
        # Obtener el nombre de la función u operador
        func_name = ctx.IDENT().getText()

        # Evaluar los argumentos
        args = [self.visit(arg) for arg in ctx.expr()]

        # Manejar operadores básicos
        if func_name in ['+', '-', '*', '/', '<', '>', '<=', '>=', '=', '<>']:
            # Operadores básicos
            if func_name == '+':
                return sum(args)
            elif func_name == '-':
                if len(args) == 1:  # Negación
                    return -args[0]
                return args[0] - sum(args[1:])
            elif func_name == '*':
                result = 1
                for arg in args:
                    result *= arg
                return result
            elif func_name == '/':
                result = args[0]
                for arg in args[1:]:
                    if arg == 0:
                        raise ZeroDivisionError("División por cero")
                    result /= arg
                return result
            elif func_name == '<':
                return all(args[i] < args[i + 1] for i in range(len(args) - 1))
            elif func_name == '>':
                return all(args[i] > args[i + 1] for i in range(len(args) - 1))
            elif func_name == '<=':
                return all(args[i] <= args[i + 1] for i in range(len(args) - 1))
            elif func_name == '>=':
                return all(args[i] >= args[i + 1] for i in range(len(args) - 1))
            elif func_name == '=':
                return all(args[i] == args[i + 1] for i in range(len(args) - 1))
            elif func_name == '<>':
                return len(args) == len(set(args))

        # Manejar funciones definidas por el usuario
        elif func_name in self.symbols:
            func = self.symbols[func_name]
            
            if "params" not in func or "body" not in func:
                raise TypeError(f"{func_name} no es una función")
            if len(args) != len(func["params"]):
                raise ValueError(f"La función {func_name} esperaba {len(func['params'])} argumentos, pero recibió {len(args)}")
            
            # Guardar el contexto actual
            saved_context = self.symbols.copy()
            
            # Crear un contexto local para los parámetros
            local_context = dict(zip(func["params"], args))
            self.symbols.update(local_context)
            
            # Evaluar el cuerpo de la función
            result = None
            for expr in func["body"]:
                result = self.visit(expr)
            
            # Restaurar el contexto original
            self.symbols = saved_context
            
            return result

        # Si el operador o función no existe, lanzar error
        else:
            raise NameError(f"Operador o función '{func_name}' no definida")



    def visitNumero(self, ctx):
        num_text = ctx.NUM().getText()  # Obtén el texto del token
        if '.' in num_text:  # Si contiene un punto, es un número decimal
            return float(num_text)
        return int(num_text)  # De lo contrario, es un entero


    def visitVariable(self, ctx):
        name = ctx.IDENT().getText()
        if name in self.symbols:
            return self.symbols[name]
        else:
            raise NameError(f"Variable {name} no definida")


    def visitCondicionalIf(self, ctx):
        condition = self.visit(ctx.expr(0))
     
        # Si la condición es verdadera, evaluar y devolver la primera rama
        if condition:
            return self.visit(ctx.expr(1))
        
        # Si la condición es falsa, evaluar y devolver la segunda rama
        return self.visit(ctx.expr(2))
        
    def visitCondicionalCond(self, ctx):
        for clause in ctx.condClause():
            cond = self.visit(clause.expr(0))
            if cond:
                return self.visit(clause.expr(1))
        raise NameError(f"Ninguna clausula es verdadera")
    
    def visitOperacionLet(self, ctx):
        local_context = {} # creamos una tabla de simbolos
        for binding in ctx.letBinding():
            variable_name = binding.IDENT().getText()
            value = self.visit(binding.expr())
            local_context[variable_name] = value
        contexto_ant = self.symbols.copy()
        self.symbols.update(local_context)
        
        result = None
        for expr in ctx.expr():
            result = self.visit(expr)

        self.symbols = contexto_ant
            
        return result
    
    def visitOperacionRead(self, ctx):
        try:
            user_input = input()
            if user_input.isdigit():
                return int(user_input)
            try:
                return float(user_input)
            except ValueError:
                return user_input # si no es numero devolvemos cadena
        except EOFError:
            raise Exception("Error leyendo entrada")
    
    def visitOperacionDisplay(self, ctx):
        value = self.visit(ctx.expr())
        print(value, end='')
        return None
    
    def visitOperacionNewLine(self, ctx):
        print()
        return None

    def visitOperacionAnd(self, ctx):
        for expr in ctx.expr():
            if not self.visit(expr):  # Si alguna expresión es falsa, devuelve False
                return False
        return True  # Todas las expresiones son verdaderas
    
    def visitOperacionOr(self, ctx):
        for expr in ctx.expr():
            if  self.visit(expr):  # Si alguna expresión es certa, devuelve True
                return True
        return False  # Todas las expresiones son falsas
    
    def visitOperacionNot(self, ctx):
        return not (self.visit(ctx.expr()))
    
    def visitTrue(self, ctx):
        return True
    
    def visitFalse(self, ctx):
        return False
    
    def visitString(self, ctx):
        return ctx.getText()[1:-1]



# Función principal para ejecutar el intérprete
def main():
    import sys
    file_name = sys.argv[1]

    # Leer el archivo .scm
    with open(file_name, 'r') as file:
        input_code = file.read()

    # Lexer y Parser
    input_stream = InputStream(input_code)
    lexer = SchemeLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = SchemeParser(token_stream)
    tree = parser.root()


    # Evaluar el programa con el Visitor
    visitor = SchemeEvalVisitor()
    results = visitor.visit(tree)

    # Imprimir los resultados
    # Imprimir los resultados
    if results:
        for result in results:
            if result is not None:
                if isinstance(result, bool):  # Verifica si es booleano
                    print("#t" if result else "#f")
                else:
                    print(result)



if __name__ == "__main__":
    main()

grammar Scheme;

// Regla inicial
root : expr+ ;

// Expresiones
expr
    : '(' 'define' '(' IDENT paramList ')'  expr+  ')'  #definicionFuncion
	| '(' 'define' IDENT expr ')'						#definicionVariable 
    | '(' IDENT expr* ')'                             #llamadaFuncion
    | '\'' '(' expr* ')'  #literalLista
	| '(' 'if' expr expr expr ')'                     #condicionalIf
    | '(' 'cond'  condClause+ ')'                      #condicionalCond
    | '(' 'car' IDENT ')'                                #operacionCar
    | '(' 'cdr' IDENT ')'                            #operacionCdr
    | '(' 'cons' expr expr ')'                            #operacionCons
    | '(' 'null?' expr ')'                             #operacionNull
    | '(' 'let' '(' letBinding* ')' expr+ ')'            #operacionLet
    | '(' 'read' ')'                                  #operacionRead
    | '(' 'display' expr ')'                          #operacionDisplay
    | '(' 'newline' ')'                               #operacionNewLine
    | '(' 'and' expr+ ')'                             #operacionAnd
    | '(' 'or' expr+ ')'                               #operacionOr
    | '(' 'not' expr ')'                                #operacionNot
    | COMMENT                                           #comment
    | IDENT                                           #variable
    | NUM                                             #numero
    | TRUE                                             #true
    | FALSE                                             #false
    | STRING                                      #string
    ;
	
paramList
    : IDENT*  // Cero o más identificadores
    ;
	
condClause
    : '(' expr expr ')' ;

letBinding
    : '(' IDENT expr ')' ;

STRING : '"' (~["\r\n])* '"';
COMMENT : ';' ~[\r\n]* -> skip ;
// Tokens
NUM : '-'? [0-9]+ ('.' [0-9]+)? ;
TRUE : '#t' ;
FALSE : '#f' ;
IDENT : [a-zA-Z+*/<>=!$%&|:?_-][a-zA-Z0-9+*/<>=!$%&|:?_-]* ;
WS : [ \t\n\r]+ -> skip ;

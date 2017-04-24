# Translators Programming Basics
## Translator from the language with the following grammar
1. <signal-program> --> <program>
2. <program> --> PROCEDURE <procedure-identifier><parameters-list> ; <block> ;
3. <block> --> <declaration> BEGIN <statements-list> END
4. <statements-list> --> <empty>
5. <parameters-list> --> (<declarations-list>) | <empty>
6. <declarations-list> --> <declaration> <declarations-list> | <empty>
7. <declaration> --> <variable-identifier> : <attribute> ;
8. <attribute> --> INTEGER | FLOAT
9. <declarations> --> <constant-declarations>
10. <constant-declarations> --> CONST <constant-declarations-list> | <empty>
11. <constant-declarations-list>  --> <constant-declaration> <constant-declarations-list> | <empty>
12. <constant-declaration> --> <constant-identifier> = <constant>;
13. <constant> --> <unsigned-integer>
14. <constant> --> - <unsigned-integer>
15. <constant-identifier> --> <identifier>
16. <variable-identifier> --> <identifier>
17. <procedure-identifier> --> <identifier>
18. <identifier> --> <letter><string>
19. <string> --> <letter><string> | <digit><string> | <empty>
20. <unsigned-integer> --> <digit><digits-string>
21. <digits-string> --> <digit><digits-string> | <empty>
22. <digit> --> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
23. <letter> --> A | B | C | D | ... | z
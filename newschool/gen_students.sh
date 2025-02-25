#!/bin/bash

#Ejecución: ./gen_students.sh < MOCK_DATA.csv > ./demo/demo_students.xml

echo "<odoo>"
echo "<data>"
echo "<!--Añadir una relación Many2one mediante 'ref', para datos de demo-->"
echo "<!--Añadir un valor calculado mediante 'eval', para datos de demo-->"

while read line
do
    name=$(echo $line | cut -d',' -f1)
    dni=$(echo $line | cut -d',' -f2)
    birth=$(echo $line | cut -d',' -f3)

    echo "<record id='student$dni' model='newschool.student'>"
    echo "<field name='name'>$name</field>"
    echo "<field name='birth_year'>$birth</field>"
    echo "<field name='dni'>$dni</field>"
    echo "<field name='classroom' ref='newschool.classroom1'></field>"
    echo "<field name='photo'>$(base64 student_default_img.jpg)</field>"
    echo "<!--<field name='last_login' eval=\"(datetime.now()+timedelta(-1)).strftime('%Y-%m-%d')\"></field>-->"
    echo "</record>"
done

echo "</data>"
echo "</odoo>"
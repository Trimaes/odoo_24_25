#!/bin/bash

echo "<odoo>"
echo "<data>"

while read line
do
    player_name=$(echo $line)
    echo "<record id='player$player_name' model='bruto_arena.player'>"
    echo "<field name='name'>$player_name</field>"
    echo "</record>"
done

echo "</data>"
echo "</odoo>"
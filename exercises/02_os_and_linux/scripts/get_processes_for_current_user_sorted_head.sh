#!/bin/bash

read -p "Sort list by memory (m) usage or CPU (c) consumption: " sort_option
read -p "Number of processes to print: " no_of_processes

echo "Get all running processes of user '$USER'"

if [ "$sort_option" == m ];
then
  echo "Process list sorted by memory usage."
  ps aux --sort=-%mem | grep $USER | head -n "$no_of_processes"
elif [ "$sort_option" == c ];
then
  echo "Process list sorted by CPU consumption."
  ps aux --sort=-%cpu | grep $USER | head -n "$no_of_processes"
else
  echo "Invalid input. Must be 'm' or 'c'."
fi
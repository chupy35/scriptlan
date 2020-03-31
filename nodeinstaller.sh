#!/bin/bash
#- Créer un script bash qui utilise votre projet
#- le script bash doit accepter un url vers un repertoire git en argument.
#- le script bash doit accepter un argument pour indiquer le port ou rouler le programme et la variable d'environnement PORT
#	- le script bash doit cloner le git, installer les dépendence node (npm install)
#	- le script bash doit partir le serveur node localement (npm start) en spécifiant le port (la variable d'environnement se nomme PORT)
# - le script bash doit exécuter votre programme sur le serveur node local (http://localhost) en vérifiant le bon port.
# - provided link: https://github.com/stevenvachon/broken-link-checker.git

github=""
port=3000

help_msg="nodeinstaller.sh -g [github repository] -p [port]"
#lack_git_url_msg="please use nodeinstaller.sh -g [url] to specify a git repository"
no_argument_msg="no argument provided"
lack_git_url_msg="lack git url"


process_petition() {
#    # install python dependency
    pip3 install -r requirements.txt

    # check repo existence before git clone
    repo_folder="$(basename "$1" .git)"
    if [ ! -d "$repo_folder" ];
    then
      git clone $1
    else
      echo "$repo_folder"
    fi

    # pre state: kill node server when terminate
    trap "kill 0" EXIT

    # start server
    cd "$repo_folder"
    npm install
    npm start -- --port $2 &
    sleep 2

    # run python script
    cd ..
    localhost_url="http://localhost:$2"
    python3 "scrapper.py" -u "$localhost_url"
#    wait
}

# make the error message shown in red color
echo_err() {
  echo -e "\033[1;31m ERROR! "$1" \033[0m"
}

# is git url provided from arguments
is_git_url_provided() {
  if [ "$1" == ""  ]
  then
    echo_err "$lack_git_url_msg"
  fi
}

# std:err append to std:out
is_valid_git_url() {
  output=$((git ls-remote --exit-code -h "$1") 2>&1)
  # inlcude error message
  if [[ "$output" = *fatal* ]]
  then
    echo_err "invalid git url"
  fi
}

# no arguments provided in arguments
is_no_arguments() {
  if [ $1 -eq 0 ]
  then
  echo_err "$no_argument_msg"
  fi
}

# contains help requirement in command line
is_help_needed() {
  if [ "$1" == "--help" ] || [ "$1" == "-h" ] ||
     [ "$2" == "--help" ] || [ "$2" == "-h" ] ||
     [ "$3" == "--help" ] || [ "$3" == "-h" ] ||
     [ "$4" == "--help" ] || [ "$4" == "-h" ]
  then
  echo $help_msg
  fi
}

# extract git url from command line
extract_git_url() {
  if [ "$1" == "--git" ] || [ "$1" == "-g" ]
  then
  github=$2
  fi
  if [ "$3" == "--git" ] || [ "$3" == "-g" ]
  then
  github=$4
  fi
  echo "extract:::::git url"
  echo "$github"
}


# extract prot from command line
extract_port() {
  if [ "$1" == "--port" ] || [ "$1" == "-p" ]
  then
  port=$2
  fi
  if [ "$3" == "--port" ] || [ "$3" == "-p" ]
  then
  port=$4
  fi
  echo "extract:::::port"
  echo "$port"
}

# extract git url, port from command line
# check whether help info is needed
extract_arguments() {
  is_help_needed $1 $2 $3 $4
  extract_git_url $1 $2 $3 $4
  extract_port $1 $2 $3 $4
}

# check if no arguments provided
is_no_arguments $#
# extract arguments
extract_arguments "$@"
# check if git url provided
is_git_url_provided "$github"
# check if git url valid
is_valid_git_url "$github"
# process
process_petition $github $port

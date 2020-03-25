#!/bin/bash
#- Créer un script bash qui utilise votre projet
#- le script bash doit accepter un url vers un repertoire git en argument.
#- le script bash doit accepter un argument pour indiquer le port ou rouler le programme et la variable d'environnement PORT
#	- le script bash doit cloner le git, installer les dépendence node (npm install)
#	- le script bash doit partir le serveur node localement (npm start) en spécifiant le port (la variable d'environnement se nomme PORT)
# - le script bash doit exécuter votre programme sur le serveur node local (http://localhost) en vérifiant le bon port.
# - provide a node repo: https://github.com/tjmonsi/simple-node-server.git

github=""
#port=3000

help_msg="nodeinstaller.sh -g [github repository] -p [port]"
lack_git_url_msg="please use nodeinstaller.sh -g [url] to specify a git repository"

process_petition() {
    # install python dependency
    pip3 install -r requirements.txt

    repo_folder="$(basename "$1" .git)"
    # check if git repository already exist
    if [ ! -d "$repo_folder" ];
    then
      git clone $1
    else
      echo "$repo_folder"
    fi

    trap "kill 0" EXIT

    cd "$repo_folder"
    npm install
    npm start -- --port $2 &
    sleep 2

    cd ..
    localhost_url="http://localhost:$2"
    python3 "scrapper.py" -u "$localhost_url"
#    wait
}

for arg in "$@"
do
    if [ "$arg" == "--help" ] || [ "$arg" == "-h" ]
    then
        echo "$help_msg"
    fi
    if [ "$arg" == "--port" ] || [ "$arg" == "-p" ]
    then
        port=$4
    fi
    if [ "$arg" == "--git" ] || [ "$arg" == "-g" ]
    then
        if [ "$2" == ""  ]
         then
            echo "lack_git_url_msg"
        else
            github=$2
        fi
    fi
done

echo "github repository: $github and port: $port"
process_petition $github $port


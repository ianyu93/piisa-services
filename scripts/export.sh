cd src 
for d in */ ; do
    echo "Exporting requirements for $d"
    cd $d
    dir_name=${PWD##*/}
    poetry export -f requirements.txt --output "$dir_name.requirements.txt" --without-hashes
    sed -i '/common @ file:\/\/\/workspaces\/piisa-services\/src\/common ; python_version >= "3.10" and python_version < "4.0"/d' "$dir_name.requirements.txt"
    cd ..
done
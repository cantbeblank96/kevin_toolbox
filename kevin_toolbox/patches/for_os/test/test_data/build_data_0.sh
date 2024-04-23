cur=`pwd`
cd ${cur}

data_dir=${cur}/data_0
rm -rf ${data_dir}

mkdir -p ${data_dir}/folder_a/
touch ${data_dir}/folder_a/fuck.json
ln -s ${data_dir}/folder_a/fuck.json ${data_dir}/folder_a/link_to_fuck.json
ln -s ${data_dir}/folder_a ${data_dir}/folder_b

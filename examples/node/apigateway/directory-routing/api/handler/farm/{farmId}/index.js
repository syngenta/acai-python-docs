exports.requirements = {
    get: {
       requiredPath: '/farm/{farmId}'
   },
    post: {
       requiredPath: '/farm/{farmId}'
   }
}

exports.put = async (request, response) => {
    response.body = {'put-farm': true}
    return response;
};

exports.delete = async (request, response) => {
    response.body = {'delete-farm': true}
    return response;
};
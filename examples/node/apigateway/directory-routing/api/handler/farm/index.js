const Farm = require('../../logic/farm');

exports.requirements = {
    post: {
       requiredBody: 'post-farm-request'
   },
    get: {
       requiredQuery: ['ownerId']
   }
}

exports.post = async (request, response) => {
    const farm = Farm.convertFromRequest(request.body);
    await farm.create();
    response.body = farm.export();
    return response;
};

exports.get = async (request, response) => {
    const farm = await Farm.getByID(request.queryParams.ownerId);
    response.body = farm.export();
    return response;
};

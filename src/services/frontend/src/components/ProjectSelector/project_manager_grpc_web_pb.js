/**
 * @fileoverview gRPC-Web generated client stub for project_manager
 * @enhanceable
 * @public
 */

// GENERATED CODE -- DO NOT EDIT!



const grpc = {};
grpc.web = require('grpc-web');

const proto = {};
proto.project_manager = require('./project_manager_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.project_manager.ProjectManagerClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

  /**
   * @private @const {?Object} The credentials to be used to connect
   *    to the server
   */
  this.credentials_ = credentials;

  /**
   * @private @const {?Object} Options for the client
   */
  this.options_ = options;
};


/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.project_manager.ProjectManagerPromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options['format'] = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

  /**
   * @private @const {?Object} The credentials to be used to connect
   *    to the server
   */
  this.credentials_ = credentials;

  /**
   * @private @const {?Object} Options for the client
   */
  this.options_ = options;
};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.project_manager.GetProjectRequest,
 *   !proto.project_manager.ProjectList>}
 */
const methodDescriptor_ProjectManager_GetProjects = new grpc.web.MethodDescriptor(
  '/project_manager.ProjectManager/GetProjects',
  grpc.web.MethodType.UNARY,
  proto.project_manager.GetProjectRequest,
  proto.project_manager.ProjectList,
  /** @param {!proto.project_manager.GetProjectRequest} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.project_manager.ProjectList.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.project_manager.GetProjectRequest,
 *   !proto.project_manager.ProjectList>}
 */
const methodInfo_ProjectManager_GetProjects = new grpc.web.AbstractClientBase.MethodInfo(
  proto.project_manager.ProjectList,
  /** @param {!proto.project_manager.GetProjectRequest} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.project_manager.ProjectList.deserializeBinary
);


/**
 * @param {!proto.project_manager.GetProjectRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.project_manager.ProjectList)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.project_manager.ProjectList>|undefined}
 *     The XHR Node Readable Stream
 */
proto.project_manager.ProjectManagerClient.prototype.getProjects =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/project_manager.ProjectManager/GetProjects',
      request,
      metadata || {},
      methodDescriptor_ProjectManager_GetProjects,
      callback);
};


/**
 * @param {!proto.project_manager.GetProjectRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.project_manager.ProjectList>}
 *     A native promise that resolves to the response
 */
proto.project_manager.ProjectManagerPromiseClient.prototype.getProjects =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/project_manager.ProjectManager/GetProjects',
      request,
      metadata || {},
      methodDescriptor_ProjectManager_GetProjects);
};


module.exports = proto.project_manager;


/**
 * @fileoverview gRPC-Web generated client stub for instance_manager
 * @enhanceable
 * @public
 */

// GENERATED CODE -- DO NOT EDIT!



const grpc = {};
grpc.web = require('grpc-web');

const proto = {};
proto.instance_manager = require('./instance_manager_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?Object} options
 * @constructor
 * @struct
 * @final
 */
proto.instance_manager.InstanceManagerClient =
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
proto.instance_manager.InstanceManagerPromiseClient =
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
 *   !proto.instance_manager.StopInstanceRequest,
 *   !proto.instance_manager.InstanceList>}
 */
const methodDescriptor_InstanceManager_StopInstances = new grpc.web.MethodDescriptor(
  '/instance_manager.InstanceManager/StopInstances',
  grpc.web.MethodType.UNARY,
  proto.instance_manager.StopInstanceRequest,
  proto.instance_manager.InstanceList,
  /** @param {!proto.instance_manager.StopInstanceRequest} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.instance_manager.InstanceList.deserializeBinary
);


/**
 * @const
 * @type {!grpc.web.AbstractClientBase.MethodInfo<
 *   !proto.instance_manager.StopInstanceRequest,
 *   !proto.instance_manager.InstanceList>}
 */
const methodInfo_InstanceManager_StopInstances = new grpc.web.AbstractClientBase.MethodInfo(
  proto.instance_manager.InstanceList,
  /** @param {!proto.instance_manager.StopInstanceRequest} request */
  function(request) {
    return request.serializeBinary();
  },
  proto.instance_manager.InstanceList.deserializeBinary
);


/**
 * @param {!proto.instance_manager.StopInstanceRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.Error, ?proto.instance_manager.InstanceList)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.instance_manager.InstanceList>|undefined}
 *     The XHR Node Readable Stream
 */
proto.instance_manager.InstanceManagerClient.prototype.stopInstances =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/instance_manager.InstanceManager/StopInstances',
      request,
      metadata || {},
      methodDescriptor_InstanceManager_StopInstances,
      callback);
};


/**
 * @param {!proto.instance_manager.StopInstanceRequest} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.instance_manager.InstanceList>}
 *     A native promise that resolves to the response
 */
proto.instance_manager.InstanceManagerPromiseClient.prototype.stopInstances =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/instance_manager.InstanceManager/StopInstances',
      request,
      metadata || {},
      methodDescriptor_InstanceManager_StopInstances);
};


module.exports = proto.instance_manager;


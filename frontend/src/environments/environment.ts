/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  //apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  apiServerUrl: 'https://vcs-badminton.onrender.com', // the running FLASK api server url
  auth0: {
    url: 'dev-i23mn0tn47hz887e.us', // the auth0 domain prefix
    audience: 'https://udacity-coffee-auth0-api/', // the audience set for the auth0 app
    clientId: 'gNSiFojbM21dZhL2UqkYnrGBf4SHwdY7', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};

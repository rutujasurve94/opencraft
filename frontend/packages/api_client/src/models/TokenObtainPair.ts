/* tslint:disable */
/* eslint-disable */
/**
 * OpenCraft Instance Manager
 * API for OpenCraft Instance Manager
 *
 * The version of the OpenAPI document: api
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface TokenObtainPair
 */
export interface TokenObtainPair {
    /**
     * 
     * @type {string}
     * @memberof TokenObtainPair
     */
    username: string;
    /**
     * 
     * @type {string}
     * @memberof TokenObtainPair
     */
    password: string;
}

export function TokenObtainPairFromJSON(json: any): TokenObtainPair {
    return TokenObtainPairFromJSONTyped(json, false);
}

export function TokenObtainPairFromJSONTyped(json: any, ignoreDiscriminator: boolean): TokenObtainPair {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'username': json['username'],
        'password': json['password'],
    };
}

export function TokenObtainPairToJSON(value?: TokenObtainPair | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'username': value.username,
        'password': value.password,
    };
}


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
 * @interface OpenEdXInstanceConfigUpdate
 */
export interface OpenEdXInstanceConfigUpdate {
    /**
     * The URL students will visit. In the future, you will also have the possibility to use your own domain name.  Example: hogwarts.opencraft.hosting
     * @type {string}
     * @memberof OpenEdXInstanceConfigUpdate
     */
    subdomain?: string;
    /**
     * The URL students will visit if you are using an external domain.
     * @type {string}
     * @memberof OpenEdXInstanceConfigUpdate
     */
    externalDomain?: string | null;
    /**
     * The name of your institution, company or project.  Example: Hogwarts Online Learning
     * @type {string}
     * @memberof OpenEdXInstanceConfigUpdate
     */
    instanceName?: string;
    /**
     * The email your instance of Open edX will be using to send emails, and where your users should send their support requests.  This needs to be a valid email.
     * @type {string}
     * @memberof OpenEdXInstanceConfigUpdate
     */
    publicContactEmail?: string;
    /**
     * URL to the privacy policy.
     * @type {string}
     * @memberof OpenEdXInstanceConfigUpdate
     */
    privacyPolicyUrl?: string;
    /**
     * The advanced theme allows users to pick a lot more details than the regular theme.Setting this flag will enable the more complex theme editor.
     * @type {boolean}
     * @memberof OpenEdXInstanceConfigUpdate
     */
    useAdvancedTheme?: boolean;
    /**
     * The theme configuration data currently being edited by the user. When finalised it willbe copied over to the final theme config which will then be deployed to the next appserverthat is launched.
     * @type {object}
     * @memberof OpenEdXInstanceConfigUpdate
     */
    draftThemeConfig?: object | null;
}

export function OpenEdXInstanceConfigUpdateFromJSON(json: any): OpenEdXInstanceConfigUpdate {
    return OpenEdXInstanceConfigUpdateFromJSONTyped(json, false);
}

export function OpenEdXInstanceConfigUpdateFromJSONTyped(json: any, ignoreDiscriminator: boolean): OpenEdXInstanceConfigUpdate {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'subdomain': !exists(json, 'subdomain') ? undefined : json['subdomain'],
        'externalDomain': !exists(json, 'external_domain') ? undefined : json['external_domain'],
        'instanceName': !exists(json, 'instance_name') ? undefined : json['instance_name'],
        'publicContactEmail': !exists(json, 'public_contact_email') ? undefined : json['public_contact_email'],
        'privacyPolicyUrl': !exists(json, 'privacy_policy_url') ? undefined : json['privacy_policy_url'],
        'useAdvancedTheme': !exists(json, 'use_advanced_theme') ? undefined : json['use_advanced_theme'],
        'draftThemeConfig': !exists(json, 'draft_theme_config') ? undefined : json['draft_theme_config'],
    };
}

export function OpenEdXInstanceConfigUpdateToJSON(value?: OpenEdXInstanceConfigUpdate | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'subdomain': value.subdomain,
        'external_domain': value.externalDomain,
        'instance_name': value.instanceName,
        'public_contact_email': value.publicContactEmail,
        'privacy_policy_url': value.privacyPolicyUrl,
        'use_advanced_theme': value.useAdvancedTheme,
        'draft_theme_config': value.draftThemeConfig,
    };
}



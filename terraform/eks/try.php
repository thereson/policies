<?php

/**
 * Astra Child Theme functions and definitions
 *
 * @link https://developer.wordpress.org/themes/basics/theme-functions/
 *
 * @package Astra Child
 * @since 1.0.0
 */

/**
 * Define Constants
 */
define('CHILD_THEME_ASTRA_CHILD_VERSION', '1.0.0');

/**
 * Enqueue styles
 */
function child_enqueue_styles()
{
    wp_enqueue_style('astra-child-theme-css', get_stylesheet_directory_uri() . '/style.css', array('astra-theme-css'), CHILD_THEME_ASTRA_CHILD_VERSION, 'all');
}
add_action('wp_enqueue_scripts', 'child_enqueue_styles', 15);

/**
 * OpenProdkt WordPress functions and definitions
 *
 * @link https://github.com/OpenProdkt/openprodkt-wp
 *
 * @package OpenProdkt WP
 * @since 1.0.0
 */
require_once '/bitnami/wordpress/wp-config.php';

// Function to retrieve PMPro data by email
function _get_member_data($email)
{
    global $wpdb;
    $pmpro_memberships_users = 'pmpro_memberships_users';
    $users = 'users';
    $members = $wpdb->get_results("
        SELECT m.* 
        FROM $wpdb->prefix$pmpro_memberships_users AS m
        JOIN $wpdb->prefix$users AS u ON u.ID = m.user_id AND u.user_email = '$email' 
        ORDER BY YEAR(enddate) ASC 
        LIMIT 1", ARRAY_A);

    // Return PMP data as an associative array
    if (count($members) > 0) {
        return $members[0];
    }
    exit;
}


// Define API URL variables
define('API_BASE_URL', 'https://api.sandbox.openprodkt.com/v1');
define('APP_AUDIT_ENDPOINT', API_BASE_URL . '/app/audit/');
define('OPENWIKI_CHECK_ENDPOINT', API_BASE_URL . '/openwiki');

function do_create_account()
{
    $apiUrl = SANDBOX_API_URL . '/app';
    $apiKey = SANDBOX_API_KEY;

    global $current_user;
    $email = $current_user->user_email;
    $mode = $_REQUEST['mode'];

    $payload = [
    'app_id'               => $mode . '-' . hash('crc32b', $email),
    'description'          => 'TEST',
    'email'                => 'test@example.com',
    'deployment_id'        => 'mariadb',
    'kubernetes_cluster'   => 'alfa-sandbox-openprodkt',
    'kubernetes_namespace' => 'demo',
    'mode'                 => 'demo',
    'digest'               => 'sha256:d67bbe7ed0a4958f1a7bbd669abe5765f7e9f734821be09b9024bc5347823d04',
    ];

    $correlation_id = wp_generate_uuid4();

    $args = [
        'method'    => 'POST',
        'timeout'   => 45,
        'sslverify' => false,
        'headers'   => [
            'Content-type'      => 'application/json',
            'x-api-key'         => $apiKey,
            'x-correlation-id'  => $correlation_id
        ],
        'body' => json_encode($payload),
    ];

    $request = wp_remote_post($apiUrl, $args);

    if (is_wp_error($request)) {
        wp_send_json_error(['message' => $request->get_error_message()], 500);
    }

    $response_code = wp_remote_retrieve_response_code($request);
    if ($response_code !== 200) {
        wp_send_json_error([
            'message' => 'API request failed.',
            'details' => wp_remote_retrieve_body($request)
        ], $response_code);
    }

    // Add action hook after creating account
    do_action('create_demo_account', $email);

    // Check deployment status directly
    $status_response = wp_remote_get(APP_AUDIT_ENDPOINT . $app_id, [
        'headers' => [
            'Content-type'      => 'application/json',
            'x-api-key'         => $apiKey,
            'x-correlation-id'  => $correlation_id
        ],
        'timeout' => 45,
    ]);

    if (is_wp_error($status_response)) {
        wp_send_json_error(['message' => 'Error checking deployment status'], 500);
    }

    $status_data = json_decode(wp_remote_retrieve_body($status_response), true);
    if (!$status_data || !isset($status_data['message'])) {
        wp_send_json_error(['message' => 'Invalid deployment status format'], 500);
    }

    $deployment_data = json_decode($status_data['message'], true);
    if (!$deployment_data) {
        wp_send_json_error(['message' => 'Invalid deployment status data'], 500);
    }

    wp_send_json_success([
        'message' => 'Account created and deployment status fetched.',
        'status' => $deployment_data['status'],
        'deployment_message' => $deployment_data['deployment_message'],
        'dns' => $deployment_data['dns'],
        'app_id' => $app_id
    ]);
}

add_action('wp_ajax_create_account', 'do_create_account');

/**
 * Enqueue the AJAX script and localize variables
 */
function enqueue_create_account_script() {
    wp_enqueue_script(
        'create-account-script',
        get_stylesheet_directory_uri() . '/functions.js',
        array('jquery'),
        '1.0',
        true
    );

    wp_localize_script('create-account-script', 'ajax_object', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce'    => wp_create_nonce('create_account_nonce')
    ));
}
add_action('wp_enqueue_scripts', 'enqueue_create_account_script');


// Shortcode to Check OpenWIKI Availability
function openwiki_app_shortcode() {
    $apiKey = SANDBOX_API_KEY;

    $args = [
        'headers' => [
            'Content-type'      => 'application/json',
            'x-api-key'         => $apiKey,
            'x-correlation-id'  => $correlation_id
        ],
    ];

    $response = wp_remote_get(OPENWIKI_CHECK_ENDPOINT, $args);

    if (is_wp_error($response)) {
        return '<p>Error checking OpenWIKI status: ' . esc_html($response->get_error_message()) . '</p>';
    }

    $data = json_decode(wp_remote_retrieve_body($response), true);

    if (isset($data['exists']) && $data['exists']) {
        return '<a href="https://openwiki.openprodkt.com" class="elementor-button">Go to OpenWIKI</a>';
    } else {
        return '<p>OpenWIKI app not available for your account.</p>';
    }
}
add_shortcode('openwiki_button', 'openwiki_app_shortcode');

// Shortcode to Create the API Data
function app_audit_shortcode() {
    $apiKey = SANDBOX_API_KEY;

    $args = [
        'headers' => [
            'Content-type'      => 'application/json',
            'x-api-key'         => $apiKey,
            'timeout'   => 45,
            'x-correlation-id'  => $correlation_id
        ],
    ];

    $endpoint = APP_AUDIT_ENDPOINT . 'test-account';


    $response = wp_remote_get($endpoint, $args);

    if (is_wp_error($response)) {
        return '<p>Error fetching app audit data: ' . esc_html($response->get_error_message()) . '</p>';
    }

    $data = json_decode(wp_remote_retrieve_body($response), true);

    if (!$data) {
        return '<p>No data available.</p>';
    }
        // Fields to exclude
    $excluded_fields = ['kubernetes_cluster', 'helm_chart', 'kubernetes_namespace'];

    // Format the output
    $output = '<div class="app-audit-info">';
    $output .= '<h3>App Audit Information</h3>';
    $output .= '<table class="audit-table">';
    foreach ($data as $key => $value) {
        if (!in_array($key, $excluded_fields)) {
            $output .= '<tr><td><strong>' . esc_html($key) . ':</strong></td><td>' . esc_html($value) . '</td></tr>';
        }
    }
    $output .= '</table>';
    $output .= '</div>';

    return $output;
}

add_shortcode('app_audit_data', 'app_audit_shortcode');

function wp_handle_membership_change($level_id, $user_id) {
    $url = 'https://765c-197-211-59-129.ngrok-free.app/pmpro';

    // Get user email
    $user_email = get_userdata($user_id)->user_email;

    // Determine the event type based on the new level ID
    if ($level_id == 0) {
        $event = 'DeleteAccount'; 
    } elseif (empty(pmpro_getMembershipLevelForUser($user_id, true))) {
        $event = 'NewAccount'; 
    } else {
        $event = 'UpgradeAccount';
    }

    // Prepare the request body
    $body = array(
        'user_id' => $user_id,
        'user_email' => $user_email,
        'event' => $event,
        'new_level_id' => $level_id,
    );

    // Send the POST request
    $response = wp_remote_post($url, array(
        'body'    => json_encode($body),
        'headers' => array('Content-Type' => 'application/json'),
    ));

    // Log errors if the request fails
    if (is_wp_error($response)) {
        error_log('API request failed: ' . $response->get_error_message());
    }
}
add_action('pmpro_after_change_membership_level', 'wp_handle_membership_change', 10, 2);

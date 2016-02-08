# coding=utf-8

PASS_LAYOUT = """
<html>
    <head>
        <title>WebSocket Checker - [PASSED] Inspection Details</title>
    </head>
    <body>
        <p>Hello!
        <p>The websocket has <strong>passed</strong> on last inspection, see the details:

        <p><ul style="list-style:none">
            <li>Total Frames Received: {TOTAL_FRAMES}</li>
            <li>Total Asserts: {TOTAL_ASSERTS}</li>
            <li>Total of validation executed: {TOTAL_VALIDATIONS}</li>
            <li>Assert frame rate: {ASSERT_RATE}%</li>
        </ul>
    </body>
</html>
"""

FAIL_LAYOUT = """
<html>
    <head>
        <title>WebSocket Checker - [FAILED] Inspection Details</title>
    </head>
    <body>
        <p>Hello!
        <p>The websocket hasn't <strong>passed</strong> on last inspection, see the details:

        <p><ul style="list-style:none">
            <li>Total Frames Received: {TOTAL_FRAMES}</li>
            <li>Total Asserts: {TOTAL_ASSERTS}</li>
            <li>Total of validation executed: {TOTAL_VALIDATIONS}</li>
            <li>Assert frame rate: {ASSERT_RATE}%</li>
        </ul>
    </body>
</html>
"""


def get_layout(layout, tags):

    if layout == 'FAIL':
        html = FAIL_LAYOUT
    elif layout == 'SUCCESS':
        html = PASS_LAYOUT
    else:
        html = ''

    for tag, value in tags.iteritems():
            html = html.replace(tag, value)

    return html

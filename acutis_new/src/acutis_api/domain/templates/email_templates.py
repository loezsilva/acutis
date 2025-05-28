from typing import Literal
from acutis_api.infrastructure.settings import settings


TEMPLATE_HEAD = """
    <html
        dir="ltr"
        xmlns="http://www.w3.org/1999/xhtml"
        xmlns:o="urn:schemas-microsoft-com:office:office"
        lang="pt-BR"
        style="height: 100%; margin: 0"
    >
    <head>
        <meta charset="UTF-8" />
        <meta content="width=device-width, initial-scale=1" name="viewport" />
        <meta content="telephone=no" name="format-detection" />
        <link
        href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i,700,700i"
        rel="stylesheet"
        />
        <link
        href="https://fonts.googleapis.com/css?family=Roboto:400,400i,700,700i"
        rel="stylesheet"
        />
        <style type="text/css">
        .logo-p-t-b {
            padding-bottom: 33px;
            padding-top: 43px;
        }
        .td-align-right {
            text-align: right;
        }
        .amp-p {
            font-size: 15px;
            color: #000;
            font-family: "open sans", "helvetica neue", helvetica, arial, sans-serif;
            line-height: 200%;
            display: block;
            text-align: left;
        }
        .amp-p-p50b {
            padding-bottom: 50px;
        }
        .text-block {
            display: inline;
            flex-basis: 47%;
            flex-direction: column;
        }
        .p-1 {
            padding-bottom: 38px;
        }
        .amp-banner {
            padding-bottom: 54px;
        }
        .text-block-p30l {
            padding-left: 30px;
        }
        a:link {
            mso-style-priority: 100 !important;
            text-decoration: underline !important;
        }
        a[x-apple-data-detectors="true"] {
            color: inherit !important;
            text-decoration: none !important;
        }
        @media only screen and (max-width: 600px) {
            a,
            p {
            line-height: 170% !important;
            }
            h1 {
            font-size: 24px !important;
            text-align: center !important;
            }
            h2 {
            font-size: 15px;
            text-align: left;
            }
            h3 {
            font-size: 16px !important;
            text-align: left !important;
            line-height: 150% !important;
            }
            h2,
            h2 a {
            font-size: 15px !important;
            text-align: left !important;
            }
            .es-content-body a,
            .es-content-body p {
            font-size: 14px !important;
            }
            [class="gmail-fix"] {
            display: none !important;
            }
            .es-left,
            .es-right {
            width: 100% !important;
            }
            .es-content,
            .es-content table {
            width: 100% !important;
            max-width: 600px !important;
            }
            .es-adapt-td {
            display: block !important;
            width: 100% !important;
            }
            .adapt-img {
            width: 100% !important;
            height: auto !important;
            }
            .adapt-img-90 {
            width: 90.3% !important;
            height: auto !important;
            }
            .adapt-img-74 {
            width: 74.6% !important;
            height: auto !important;
            }
            .adapt-img-69 {
            width: 69.8% !important;
            height: auto !important;
            }
            .adapt-img-62 {
            width: 62.5% !important;
            height: auto !important;
            }
            .es-m-p0 {
            padding: 0 !important;
            }
            .es-m-p0r {
            padding-right: 0 !important;
            }
            .es-m-p0l {
            padding-left: 0 !important;
            }
            .es-m-p0t {
            padding-top: 0 !important;
            }
            .es-m-p0b {
            padding-bottom: 0 !important;
            }
            .es-m-p5 {
            padding-top: 5px !important;
            padding-bottom: 5px !important;
            padding-left: 5px !important;
            padding-right: 5px !important;
            }
            .es-m-p5t {
            padding-top: 5px !important;
            }
            .es-m-p5l {
            padding-left: 5px !important;
            }
            .es-m-p5r {
            padding-right: 5px !important;
            }
            .es-m-p10l {
            padding-left: 10px !important;
            }
            .es-m-p10r {
            padding-right: 10px !important;
            }
            .es-m-p10b {
            padding-bottom: 10px !important;
            }
            .es-m-p15t {
            padding-top: 15px !important;
            }
            .es-m-p15l {
            padding-left: 15px !important;
            }
            .es-m-p15r {
            padding-right: 15px !important;
            }
            .es-m-p15 {
            padding-top: 15px !important;
            padding-bottom: 15px !important;
            padding-left: 15px !important;
            padding-right: 15px !important;
            }
            .es-m-p20b {
            padding-bottom: 20px !important;
            }
            .es-m-p20l {
            padding-left: 20px !important;
            }
            .es-m-p20r {
            padding-right: 20px !important;
            }
            .es-m-p20t {
            padding-top: 20px !important;
            }
            .es-m-p22t {
            padding-top: 22px !important;
            }
            .es-m-p25l {
            padding-left: 25px !important;
            }
            .es-m-p25r {
            padding-right: 25px !important;
            }
            .es-m-p30t {
            padding-top: 30px !important;
            }
            .es-m-p30b {
            padding-bottom: 30px !important;
            }
            .es-m-p40t {
            padding-top: 40px !important;
            }
            .es-m-p40b {
            padding-bottom: 40px !important;
            }
            .es-m-p40r {
            padding-right: 20px !important;
            }
            .es-m-p60l {
            padding-left: 60px !important;
            }
            .es-m-p60b {
            padding-bottom: 60px !important;
            }
            .es-m-p80t {
            padding-top: 80px !important;
            }
            .es-m-p100b {
            padding-bottom: 100px !important;
            }
            .es-m-p105r {
            padding-right: 75px !important;
            }
            .es-m-p125r {
            padding-right: 105px !important;
            }
            .es-m-p155r {
            padding-right: 135px !important;
            }
            .es-m-p155l {
            padding-left: 135px !important;
            }
            .m-bg {
            background-color: #eee !important;
            }
            h4 {
            font-size: 10px !important;
            line-height: 150% !important;
            }
            .m-logo-m {
            width: 140px !important;
            }
            .m-bg-none {
            background-image: none !important;
            }
            .m-border {
            border: 4px solid #58a449 !important;
            background-color: #5a5750 !important;
            }
            .m-bg-80 {
            background-size: 80% auto !important;
            background-position: center center !important;
            }
            .m-bg-bottom {
            background-size: auto 68% !important;
            }
            .m-bg-auto {
            background-size: auto 100% !important;
            }
            .m-bg-120 {
            background-size: 110% auto !important;
            }
            .m-bg-100-100 {
            background-size: 100% 100% !important;
            }
            .m-br-none {
            border-radius: 0 !important;
            }
            .m-btn-m {
            width: 200px !important;
            height: auto !important;
            }
            .banner-left-p {
            padding-left: 0;
            }
            .logo-p-t-b {
            padding-top: 20px;
            padding-bottom: 20px;
            }
            .amp-p {
            font-size: 14px;
            line-height: 170%;
            }
            h2 a {
            text-align: left;
            }
            .es-content-body h2 a {
            font-size: 15px;
            }
        }
        </style>
    </head>
    """


def verify_become_general(token: str):
    template = (
        TEMPLATE_HEAD
        + f"""
            <!DOCTYPE html>
<html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
    <meta charset="UTF-8" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <!--[if !mso]><!-- -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <!--<![endif]-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="format-detection" content="telephone=no" />
    <meta name="format-detection" content="date=no" />
    <meta name="format-detection" content="address=no" />
    <meta name="format-detection" content="email=no" />
    <meta name="x-apple-disable-message-reformatting" />
    <link href="https://fonts.googleapis.com/css?family=DM+Serif+Display:ital,wght@0,400;0,400" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css?family=Fira+Sans:ital,wght@0,400;0,400;0,500" rel="stylesheet" />
    <title></title>

</head>

<body class="body pc-font-alt"
    style="width: 100% !important; min-height: 100% !important; margin: 0 !important; padding: 0 !important; line-height: 1.5; color: #2D3A41; mso-line-height-rule: exactly; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-variant-ligatures: normal; text-rendering: optimizeLegibility; -moz-osx-font-smoothing: grayscale; background-color: #121924;"
    bgcolor="#121924">
    <table class="pc-project-body" style="table-layout: fixed; min-width: 600px; background-color: #121924;"
        bgcolor="#121924" width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
        <tr>
            <td align="center" valign="top">
                <table class="pc-project-container" align="center" width="600" style="width: 600px; max-width: 600px;"
                    border="0" cellpadding="0" cellspacing="0" role="presentation">
                    <tr>
                        <td style="padding: 20px 0px 20px 0px;" align="left" valign="top">
                            <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%"
                                style="width: 100%;">
                                <tr>
                                    <td valign="top">
                                        <!-- BEGIN MODULE: Header 1 -->
                                        <table width="100%" border="0" cellspacing="0" cellpadding="0"
                                            role="presentation">
                                            <tr>
                                                <td style="padding: 0px 0px 0px 0px;">
                                                    <table width="100%" border="0" cellspacing="0" cellpadding="0"
                                                        role="presentation">
                                                        <tr>
                                                            <!--[if !gte mso 9]><!-- -->
                                                            <td valign="top"
                                                                class="pc-w520-padding-27-30-27-30 pc-w620-padding-32-35-32-35"
                                                                style="background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/template_bg_blue.png'); background-size: cover; background-position: center; background-repeat: no-repeat; padding: 37px 40px 37px 40px; border-radius: 0px; background-color: #1B1B1B;"
                                                                bgcolor="#1B1B1B"
                                                                background="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/template_bg_blue.png">
                                                                <!--<![endif]-->
                                                                <!--[if gte mso 9]>
                <td valign="top" align="center" style="background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/template_bg_blue.png'); background-size: cover; background-position: center; background-repeat: no-repeat; background-color: #1B1B1B; border-radius: 0px;" bgcolor="#1B1B1B" background="images/image-1737232277422.png">
            <![endif]-->
                                                                <!--[if gte mso 9]>
                <v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width: 600px;">
                    <v:fill src="images/image-1737232277422.png" color="#1B1B1B" type="frame" size="1,1" aspect="atleast" origin="0,0" position="0,0"/>
                    <v:textbox style="mso-fit-shape-to-text: true;" inset="0,0,0,0">
                        <div style="font-size: 0; line-height: 0;">
                            <table width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation">
                                <tr>
                                    <td style="font-size: 14px; line-height: 1.5;" valign="top">
                                        <p style="margin:0;mso-hide:all"><o:p xmlns:o="urn:schemas-microsoft-com:office:office">&nbsp;</o:p></p>
                                        <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
                                            <tr>
                                                <td colspan="3" height="37" style="line-height: 1px; font-size: 1px;">&nbsp;</td>
                                            </tr>
                                            <tr>
                                                <td width="40" valign="top" style="line-height: 1px; font-size: 1px;">&nbsp;</td>
                                                <td valign="top" align="left">
                <![endif]-->
                                                                <table width="100%" border="0" cellpadding="0"
                                                                    cellspacing="0" role="presentation">
                                                                    <tr>
                                                                        <td align="center" valign="top"
                                                                            style="padding: 0px 0px 50px 0px;">
                                                                            <img src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/template_logo.png"
                                                                                width="280" height="54" alt=""
                                                                                style="display: block; outline: 0; line-height: 100%; -ms-interpolation-mode: bicubic; width: 280px; height: auto; max-width: 100%; border: 0;" />
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                                <table width="100%" border="0" cellpadding="0"
                                                                    cellspacing="0" role="presentation">
                                                                    <tr>
                                                                        <td class="pc-w620-spacing-0-0-10-0"
                                                                            align="left" valign="top"
                                                                            style="padding: 0px 0px 17px 0px;">
                                                                            <table border="0" cellpadding="0"
                                                                                cellspacing="0" role="presentation"
                                                                                width="100%"
                                                                                style="border-collapse: separate; border-spacing: 0; margin-right: auto; margin-left: auto;">
                                                                                <tr>
                                                                                    <td valign="top" align="left">
                                                                                        <div class="pc-font-alt"
                                                                                            style="text-decoration: none;">
                                                                                            <div
                                                                                                style="font-size:28px;line-height:44px;text-align:center;text-align-last:center;color:#c98f00;letter-spacing:-0.2px;font-weight:400;font-style:normal;font-variant-ligatures:normal;">
                                                                                                <div
                                                                                                    style="margin-bottom: 0px;">
                                                                                                    <span
                                                                                                        style="font-family: 'DM Serif Display', Arial, Helvetica, sans-serif; font-size: 28px; line-height: 44px; text-decoration: none; text-transform: none;">Dê
                                                                                                        o próximo passo
                                                                                                        e torne-se um
                                                                                                        General Oficial
                                                                                                        do Exército de
                                                                                                        São
                                                                                                        Miguel!</span>
                                                                                                </div>
                                                                                            </div>
                                                                                        </div>
                                                                                    </td>
                                                                                </tr>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                                <!--[if gte mso 9]>
                                                </td>
                                                <td width="40" style="line-height: 1px; font-size: 1px;" valign="top">&nbsp;</td>
                                            </tr>
                                            <tr>
                                                <td colspan="3" height="37" style="line-height: 1px; font-size: 1px;">&nbsp;</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </div>
                        <p style="margin:0;mso-hide:all"><o:p xmlns:o="urn:schemas-microsoft-com:office:office">&nbsp;</o:p></p>
                    </v:textbox>
                </v:rect>
                <![endif]-->
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                        <!-- END MODULE: Header 1 -->
                                    </td>
                                </tr>
                                <tr>
                                    <td valign="top">
                                        <!-- BEGIN MODULE: Call to action 1 -->
                                        <table width="100%" border="0" cellspacing="0" cellpadding="0"
                                            role="presentation">
                                            <tr>
                                                <td style="padding: 0px 0px 0px 0px;">
                                                    <table width="100%" border="0" cellspacing="0" cellpadding="0"
                                                        role="presentation">
                                                        <tr>
                                                            <td valign="top"
                                                                class="pc-w520-padding-30-40-30-40 pc-w620-padding-35-50-35-50"
                                                                style="padding: 40px 60px 40px 60px; border-radius: 0px; background-color: #121924;"
                                                                bgcolor="#121924">
                                                                <table width="100%" border="0" cellpadding="0"
                                                                    cellspacing="0" role="presentation">
                                                                    <tr>
                                                                        <td align="center" valign="top"
                                                                            style="padding: 0px 0px 20px 0px;">
                                                                            <table border="0" cellpadding="0"
                                                                                cellspacing="0" role="presentation"
                                                                                width="100%"
                                                                                style="border-collapse: separate; border-spacing: 0; margin-right: auto; margin-left: auto;">
                                                                                <tr>
                                                                                    <td valign="top" align="center">
                                                                                        <div class="pc-font-alt"
                                                                                            style="text-decoration: none;">
                                                                                            <div
                                                                                                style="font-size:18px;line-height:28px;text-align:center;text-align-last:center;color:#ffffff;letter-spacing:-0.2px;font-weight:400;font-style:normal;font-variant-ligatures:normal;">
                                                                                                <div
                                                                                                    style="margin-bottom: 0px;">
                                                                                                    <span
                                                                                                        style="font-family: 'Fira Sans', Arial, Helvetica, sans-serif; font-size: 18px; line-height: 28px; text-decoration: none; text-transform: uppercase;">O
                                                                                                        próximo passo é
                                                                                                        muito simples:
                                                                                                    </span><span
                                                                                                        style="font-family: 'Fira Sans', Arial, Helvetica, sans-serif; color: rgb(195, 195, 195); font-size: 18px; line-height: 28px; text-decoration: none; text-transform: none;">Basta
                                                                                                        clicar no link
                                                                                                        abaixo, para
                                                                                                        confirmar seus
                                                                                                        dados e se
                                                                                                        tornar um
                                                                                                        GENERAL
                                                                                                        OFICIAL!</span>
                                                                                                </div>
                                                                                            </div>
                                                                                        </div>
                                                                                    </td>
                                                                                </tr>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                                <table width="100%" border="0" cellpadding="0"
                                                                    cellspacing="0" role="presentation">
                                                                    <tr>
                                                                        <td align="center">
                                                                            <table
                                                                                class="pc-width-hug pc-w620-gridCollapsed-1"
                                                                                align="center" border="0"
                                                                                cellpadding="0" cellspacing="0"
                                                                                role="presentation">
                                                                                <tr
                                                                                    class="pc-grid-tr-first pc-grid-tr-last">
                                                                                    <td class="pc-grid-td-first pc-grid-td-last pc-w620-itemsSpacings-0-20"
                                                                                        valign="top"
                                                                                        style="padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;">
                                                                                        <table
                                                                                            style="border-collapse: separate; border-spacing: 0;"
                                                                                            border="0" cellpadding="0"
                                                                                            cellspacing="0"
                                                                                            role="presentation">
                                                                                            <tr>
                                                                                                <td align="center"
                                                                                                    valign="top">
                                                                                                    <table
                                                                                                        align="center"
                                                                                                        width="100%"
                                                                                                        border="0"
                                                                                                        cellpadding="0"
                                                                                                        cellspacing="0"
                                                                                                        role="presentation"
                                                                                                        style="width: 100%;">
                                                                                                        <tr>
                                                                                                            <td align="center"
                                                                                                                valign="top">
                                                                                                                <table
                                                                                                                    width="100%"
                                                                                                                    border="0"
                                                                                                                    cellpadding="0"
                                                                                                                    cellspacing="0"
                                                                                                                    role="presentation">
                                                                                                                    <tr>
                                                                                                                        <th valign="top"
                                                                                                                            align="center"
                                                                                                                            style="text-align: center; font-weight: normal; line-height: 1;">
                                                                                                                            <!--[if mso]>
        <table border="0" cellpadding="0" cellspacing="0" role="presentation" align="center" width="283" style="border-collapse: separate; border-spacing: 0; margin-right: auto; margin-left: auto;">
            <tr>
                <td valign="middle" align="center" style="width: 283px; border-radius: 100px 100px 100px 100px; border: 1px solid transparent; background-color: #19c78a; text-align:center; color: #ffffff; padding: 14px 18px 14px 18px; mso-padding-left-alt: 0; margin-left:18px;" bgcolor="#19c78a">
                                    <a class="pc-font-alt" style="display: inline-block; text-decoration: none; font-variant-ligatures: normal; font-family: 'Fira Sans', Arial, Helvetica, sans-serif; text-align: center;" href="https://cadastro.institutohesed.org.br/membro-exercito/landing-page-membros?alistamento_esm_token={token}" target="_blank"><span style="font-size:16px;line-height:24px;color:#ffffff;letter-spacing:-0.2px;font-weight:500;font-style:normal;display:inline-block;font-variant-ligatures:normal;"><span style="display: inline-block; margin-bottom: 0px;"><span style="font-family: 'Fira Sans', Arial, Helvetica, sans-serif; font-size: 16px; line-height: 24px; text-decoration: none; text-transform: none;">QUERO DAR ESSE PASSO</span></span></span></a>
                                </td>
            </tr>
        </table>
        <![endif]-->
                                                                                                                            <!--[if !mso]><!-- -->
                                                                                                                            <a style="display: inline-block; box-sizing: border-box; border: 1px solid transparent; border-radius: 100px 100px 100px 100px; background-color: #19c78a; padding: 14px 18px 14px 18px; width: 283px; font-family: 'Fira Sans', Arial, Helvetica, sans-serif; vertical-align: top; text-align: center; text-align-last: center; text-decoration: none; -webkit-text-size-adjust: none; mso-hide: all;"
                                                                                                                                href="https://cadastro.institutohesed.org.br/membro-exercito/landing-page-membros?alistamento_esm_token={token}"
                                                                                                                                target="_blank"><span
                                                                                                                                    style="font-size:16px;line-height:24px;color:#ffffff;letter-spacing:-0.2px;font-weight:500;font-style:normal;display:inline-block;font-variant-ligatures:normal;"><span
                                                                                                                                        style="display: inline-block; margin-bottom: 0px;"><span
                                                                                                                                            style="font-family: 'Fira Sans', Arial, Helvetica, sans-serif; font-size: 16px; line-height: 24px; text-decoration: none; text-transform: none;">QUERO
                                                                                                                                            DAR
                                                                                                                                            ESSE
                                                                                                                                            PASSO</span></span></span></a>
                                                                                                                            <!--<![endif]-->
                                                                                                                        </th>
                                                                                                                    </tr>
                                                                                                                </table>
                                                                                                            </td>
                                                                                                        </tr>
                                                                                                    </table>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                            </table>
                                                                        </td>
                                                                    </tr>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                        <!-- END MODULE: Call to action 1 -->
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>

</html>
        """
    )

    return template


def ativar_conta_email_template(nome: str, token: str):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body
            style="
            height: 100%;
            width: 100%;
            font-family: roboto, 'helvetica neue', helvetica, arial, sans-serif;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            margin: 0;
            "
        >
            <div
            dir="ltr"
            class="es-wrapper-color"
            lang="pt"
            style="background-color: #ffffff"
            >
            <table
                class="es-wrapper"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                margin: 0;
                width: 100%;
                height: 100%;
                background-repeat: repeat;
                background-position: center top;
                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/particula_plano_de_fundo.png');
                background-color: #ffffff;
                "
                role="none"
            >
                <tr style="border-collapse: collapse">
                <td valign="top" style="margin: 0">
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td align="center" style="margin: 0">
                        <table
                            bgcolor="#ffffff"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            role="none"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p0t"
                                align="left"
                                style="
                                margin: 0;
                                background-position: center bottom;
                                background-color: transparent;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center bottom;
                                        background-color: transparent;
                                        "
                                        bgcolor="transparent"
                                        role="none"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; display: none"
                                        ></td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20b"
                                align="left"
                                style="
                                margin: 0;
                                border-radius: 30px 30px 0px 0px;
                                background-color: #515151;
                                "
                                bgcolor="#515151"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-size: 100%;
                                        background-position: left top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="logo-p-t-b"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/logo_hesed.png"
                                                alt="Foto da Logomarca do Instituto Hesed"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                height="100"
                                                title="Foto da Logomarca do Instituto Hesed"
                                                class="m-logo-m adapt-img"
                                                sizes="(max-width:600px) 140px, 204px"
                                            /></a>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="es-m-p30b amp-banner"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/bg_bible.jpg"
                                                alt
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                sizes="(max-width:600px) 80vw, 373px"
                                                class="adapt-img"
                                                width="700"
                                            /></a>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20l es-m-p20r es-m-p40b m-bg-none"
                                align="left"
                                style="
                                margin: 0;
                                padding-top: 40px;
                                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/card_outline.jpg');
                                background-position: center top;
                                background-color: #ffffff;
                                background-repeat: no-repeat;
                                padding-right: 80px;
                                padding-left: 80px;
                                padding-bottom: 125px;
                                "
                                bgcolor="#ffffff"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 540px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            <h1
                                            style="
                                                margin: 0;
                                                line-height: 43.2px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 36px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            <strong>Seja bem vindo(a)</strong>
                                            </h1>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            &nbsp; &nbsp;
                                            <h3
                                            style="
                                                margin: 0;
                                                line-height: 21.6px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 18px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            Querido(a) {nome}.
                                            </h3>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            É com grande alegria que te damos as
                                            boas-vindas!
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Estamos muito felizes em tê-lo(a) conosco
                                            e agradecemos por se juntar à nossa missão
                                            de promover a caridade e os valores
                                            cristãos em nossa comunidade.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            A partir de agora, você estará
                                            conectado(a) a tudo o que fazemos,
                                            recebendo informações e oportunidades para
                                            participar ativamente em nossa comunidade
                                            e ações.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Que esta nova caminhada seja abençoada e
                                            repleta de realizações. Estamos aqui para
                                            apoiar e caminhar junto com você!
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="
                                            margin: 0;
                                            padding-top: 25px;
                                            padding-bottom: 25px;
                                            font-size: 0px;
                                            "
                                        >
                                            <a
                                            href="https://cadastro.institutohesed.org.br/?token={token}"
                                            target="_blank"
                                            style="display: inline-block"
                                            >
                                            <img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/btn_concluir_cadastro.jpg"
                                                alt=""
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                class="adapt-img"
                                                width="250"
                                            />
                                            </a>
                                        </td>
                                        </tr>
                                        <tr
                                        class="es-visible-simple-html-only"
                                        style="border-collapse: collapse"
                                        >
                                        <td
                                            align="center"
                                            valign="top"
                                            style="margin: 0; width: 700px"
                                        >
                                            <table
                                            cellpadding="0"
                                            cellspacing="0"
                                            width="100%"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                                border-collapse: separate;
                                                border-spacing: 0px;
                                                background-position: center top;
                                                background-color: #515151;
                                                border-radius: 0 0 30px 30px;
                                            "
                                            bgcolor="#515151"
                                            role="presentation"
                                            >
                                            <tr style="border-collapse: collapse">
                                                <td
                                                align="center"
                                                style="margin: 0; padding-top: 20px"
                                                >
                                                <h2
                                                    style="
                                                    margin: 0;
                                                    line-height: 28.8px;
                                                    mso-line-height-rule: exactly;
                                                    font-family: 'open sans',
                                                        'helvetica neue', helvetica,
                                                        arial, sans-serif;
                                                    font-size: 24px;
                                                    font-style: normal;
                                                    font-weight: bold;
                                                    color: #ffffff;
                                                    "
                                                >
                                                    Instituto Hesed | Casa Mãe
                                                </h2>
                                                </td>
                                            </tr>
                                            <tr style="border-collapse: collapse">
                                                <td
                                                align="left"
                                                style="
                                                    margin: 0;
                                                    padding-top: 30px;
                                                    padding-bottom: 40px;
                                                    padding-right: 110px;
                                                    padding-left: 110px;
                                                "
                                                class="es-m-p20l es-m-p20r"
                                                >
                                                <p
                                                    style="
                                                    margin: 0;
                                                    -webkit-text-size-adjust: none;
                                                    -ms-text-size-adjust: none;
                                                    mso-line-height-rule: exactly;
                                                    font-family: roboto,
                                                        'helvetica neue', helvetica,
                                                        arial, sans-serif;
                                                    line-height: 28px;
                                                    color: #ffffff;
                                                    font-size: 14px;
                                                    letter-spacing: 1px;
                                                    "
                                                >
                                                    Av. Dionisio Leonel Alencar, 1443 -
                                                    Parque Santa Maria<br />Cep:
                                                    60873-073 | Fortaleza – Ceará<br />(85)
                                                    3274-4513 -
                                                    contato@institutohesed.org.br
                                                </p>
                                                </td>
                                            </tr>
                                            </table>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    ></table>
                </td>
                </tr>
            </table>
            </div>
        </body>
        </html>
    """
    )
    return template


def reminder_active_account_email_template(name, token):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body
            style="
            height: 100%;
            width: 100%;
            font-family: roboto, 'helvetica neue', helvetica, arial, sans-serif;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            margin: 0;
            "
        >
            <div
            dir="ltr"
            class="es-wrapper-color"
            lang="pt"
            style="background-color: #ffffff"
            >
            <table
                class="es-wrapper"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                margin: 0;
                width: 100%;
                height: 100%;
                background-repeat: repeat;
                background-position: center top;
                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/particula_plano_de_fundo.png');
                background-color: #ffffff;
                "
                role="none"
            >
                <tr style="border-collapse: collapse">
                <td valign="top" style="margin: 0">
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td align="center" style="margin: 0">
                        <table
                            bgcolor="#ffffff"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            role="none"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p0t"
                                align="left"
                                style="
                                margin: 0;
                                background-position: center bottom;
                                background-color: transparent;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center bottom;
                                        background-color: transparent;
                                        "
                                        bgcolor="transparent"
                                        role="none"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; display: none"
                                        ></td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20b"
                                align="left"
                                style="
                                margin: 0;
                                border-radius: 30px 30px 0px 0px;
                                background-color: #515151;
                                "
                                bgcolor="#515151"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-size: 100%;
                                        background-position: left top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="logo-p-t-b"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/logo_hesed.png"
                                                alt="Foto da logomarca do Instituto Hesed"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                height="100"
                                                title="Foto da logomarca do Instituto Hesed"
                                                class="m-logo-m adapt-img"
                                                sizes="(max-width:600px) 140px, 204px"
                                            /></a>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20l es-m-p20r es-m-p40b m-bg-none"
                                align="left"
                                style="
                                margin: 0;
                                padding-top: 40px;
                                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/card_outlined_gray.jpg');
                                background-position: center top;
                                background-color: #ffffff;
                                background-repeat: no-repeat;
                                padding-right: 80px;
                                padding-left: 80px;
                                padding-bottom: 125px;
                                "
                                bgcolor="#ffffff"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 540px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            <h1
                                            style="
                                                margin: 0;
                                                line-height: 43.2px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 36px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            <strong>Ativação do cadastro</strong>
                                            </h1>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            &nbsp; &nbsp;
                                            <h3
                                            style="
                                                margin: 0;
                                                line-height: 21.6px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 18px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            Querido(a) {name}.
                                            </h3>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Notamos que você iniciou seu cadastro em
                                            nosso sistema há alguns dias, mas ainda
                                            não o completou. Gostaríamos de
                                            convidá-lo(a) a finalizar o processo e
                                            ativar sua conta para que possa aproveitar
                                            todos os benefícios de fazer parte da
                                            nossa comunidade no Instituto Hesed.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            ></p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Sua participação é muito importante para nós, e estamos ansiosos para ter você mais próximo(a) de nossa missão de promover a caridade.<br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Se precisar de ajuda, estamos à disposição!
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    style="
                                        margin: 0;
                                        padding-top: 25px;
                                        padding-bottom: 25px;
                                        font-size: 0px;
                                    "
                                    >
                                    <a
                                        href="{settings.URL_FRONTEND_CADASTRO}/?token={token}"
                                        target="_blank"
                                        style="display: inline-block"
                                    >
                                        <img
                                        src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/btn_concluir_cadastro.jpg"
                                        alt
                                        style="
                                            display: block;
                                            border: 0;
                                            outline: none;
                                            text-decoration: none;
                                            -ms-interpolation-mode: bicubic;
                                        "
                                        class="adapt-img"
                                        width="235"
                                        />
                                    </a>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr
                                    class="es-visible-simple-html-only"
                                    style="border-collapse: collapse"
                                >
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: separate;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        background-color: #515151;
                                        border-radius: 0 0 30px 30px;
                                        "
                                        bgcolor="#515151"
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-top: 20px"
                                        >
                                            <h2
                                            style="
                                                margin: 0;
                                                line-height: 28.8px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 24px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #ffffff;
                                            "
                                            >
                                            Instituto Hesed | Casa Mãe
                                            </h2>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="
                                            margin: 0;
                                            padding-top: 30px;
                                            padding-bottom: 40px;
                                            padding-right: 110px;
                                            padding-left: 110px;
                                            "
                                            class="es-m-p20l es-m-p20r"
                                        >
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 28px;
                                                color: #ffffff;
                                                font-size: 14px;
                                                letter-spacing: 1px;
                                            "
                                            >
                                            Av. Dionisio Leonel Alencar, 1443<br />Parque
                                            Santa Maria<br />Cep: 60873-073<br />Fortaleza
                                            – Ceará<br />(85) 3274-4513<br />contato@institutohesed.org.br
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        ></table>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </div>
        </body>
        </html>
    """
    )

    return template


def excluir_conta_email_template(name, token):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body
            style="
            height: 100%;
            width: 100%;
            font-family: roboto, 'helvetica neue', helvetica, arial, sans-serif;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            margin: 0;
            "
        >
            <div
            dir="ltr"
            class="es-wrapper-color"
            lang="pt"
            style="background-color: #ffffff"
            >
            <table
                class="es-wrapper"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                margin: 0;
                width: 100%;
                height: 100%;
                background-repeat: repeat;
                background-position: center top;
                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/particula_plano_de_fundo.png');
                background-color: #ffffff;
                "
                role="none"
            >
                <tr style="border-collapse: collapse">
                <td valign="top" style="margin: 0">
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td align="center" style="margin: 0">
                        <table
                            bgcolor="#ffffff"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            role="none"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p0t"
                                align="left"
                                style="
                                margin: 0;
                                background-position: center bottom;
                                background-color: transparent;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center bottom;
                                        background-color: transparent;
                                        "
                                        bgcolor="transparent"
                                        role="none"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; display: none"
                                        ></td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20b"
                                align="left"
                                style="
                                margin: 0;
                                border-radius: 30px 30px 0px 0px;
                                background-color: #515151;
                                "
                                bgcolor="#515151"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-size: 100%;
                                        background-position: left top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="logo-p-t-b"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/logo_hesed.png"
                                                alt="Foto da Logomarca do Instituto Hesed"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                height="100"
                                                title="Foto da Logomarca do Instituto Hesed"
                                                class="m-logo-m adapt-img"
                                                sizes="(max-width:600px) 140px, 204px"
                                            /></a>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="es-m-p30b amp-banner"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/bg_bible.jpg"
                                                alt
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                sizes="(max-width:600px) 80vw, 373px"
                                                class="adapt-img"
                                                width="700"
                                            /></a>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20l es-m-p20r es-m-p40b m-bg-none"
                                align="left"
                                style="
                                margin: 0;
                                padding-top: 40px;
                                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/card_outline.jpg');
                                background-position: center top;
                                background-color: #ffffff;
                                background-repeat: no-repeat;
                                padding-right: 80px;
                                padding-left: 80px;
                                padding-bottom: 125px;
                                "
                                bgcolor="#ffffff"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 540px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            <h1
                                            style="
                                                margin: 0;
                                                line-height: 43.2px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 36px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            <strong>Confirmação de exclusão de conta. </strong>
                                            </h1>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            &nbsp; &nbsp;
                                            <h3
                                            style="
                                                margin: 0;
                                                line-height: 21.6px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 18px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            Querido(a) {name}.
                                            </h3>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Caso queira realmente deletar sua conta clique em confirmar, caso contrário, apenas ignore.
                                            <br />
                                            </p>
					                        <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Se você tiver alguma dúvida ou precisar de ajuda, não hesite em entrar em contato com nossa equipe de suporte ao cliente, que está disponível para ajudá-lo com qualquer problema ou preocupação.
                                            <br />
                                            </p>
                                            <div style="text-align: center; margin: 20px 0;">
                                                <a href="{settings.URL_FRONTEND_CADASTRO}?token_deletar_conta={token}" target="_blank" style="display: inline-block; padding: 15px 25px; background-color: #f44336; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 0 10px;">
                                                    Confirmar
                                                </a>
                                            </div>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr
                                        class="es-visible-simple-html-only"
                                        style="border-collapse: collapse"
                                        >
                                        <td
                                            align="center"
                                            valign="top"
                                            style="margin: 0; width: 700px"
                                        >
                                            <table
                                            cellpadding="0"
                                            cellspacing="0"
                                            width="100%"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                                border-collapse: separate;
                                                border-spacing: 0px;
                                                background-position: center top;
                                                background-color: #515151;
                                                border-radius: 0 0 30px 30px;
                                            "
                                            bgcolor="#515151"
                                            role="presentation"
                                            >
                                            <tr style="border-collapse: collapse">
                                                <td
                                                align="center"
                                                style="margin: 0; padding-top: 20px"
                                                >
                                                <h2
                                                    style="
                                                    margin: 0;
                                                    line-height: 28.8px;
                                                    mso-line-height-rule: exactly;
                                                    font-family: 'open sans',
                                                        'helvetica neue', helvetica,
                                                        arial, sans-serif;
                                                    font-size: 24px;
                                                    font-style: normal;
                                                    font-weight: bold;
                                                    color: #ffffff;
                                                    "
                                                >
                                                    Instituto Hesed | Casa Mãe
                                                </h2>
                                                </td>
                                            </tr>
                                            <tr style="border-collapse: collapse">
                                                <td
                                                align="left"
                                                style="
                                                    margin: 0;
                                                    padding-top: 30px;
                                                    padding-bottom: 40px;
                                                    padding-right: 110px;
                                                    padding-left: 110px;
                                                "
                                                class="es-m-p20l es-m-p20r"
                                                >
                                                <p
                                                    style="
                                                    margin: 0;
                                                    -webkit-text-size-adjust: none;
                                                    -ms-text-size-adjust: none;
                                                    mso-line-height-rule: exactly;
                                                    font-family: roboto,
                                                        'helvetica neue', helvetica,
                                                        arial, sans-serif;
                                                    line-height: 28px;
                                                    color: #ffffff;
                                                    font-size: 14px;
                                                    letter-spacing: 1px;
                                                    "
                                                >
                                                    Av. Dionisio Leonel Alencar, 1443 -
                                                    Parque Santa Maria<br />Cep:
                                                    60873-073 | Fortaleza – Ceará<br />(85)
                                                    3274-4513 -
                                                    contato@institutohesed.org.br
                                                </p>
                                                </td>
                                            </tr>
                                            </table>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    ></table>
                </td>
                </tr>
            </table>
            </div>
        </body>
        </html>
    """
    )
    return template


def reset_password_email_template(name, token, url_redirect):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body
            style="
            height: 100%;
            width: 100%;
            font-family: roboto, 'helvetica neue', helvetica, arial, sans-serif;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            margin: 0;
            "
        >
            <div
            dir="ltr"
            class="es-wrapper-color"
            lang="pt"
            style="background-color: #ffffff"
            >
            <table
                class="es-wrapper"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                margin: 0;
                width: 100%;
                height: 100%;
                background-repeat: repeat;
                background-position: center top;
                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/particula_plano_de_fundo.png');
                background-color: #ffffff;
                "
                role="none"
            >
                <tr style="border-collapse: collapse">
                <td valign="top" style="margin: 0">
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td align="center" style="margin: 0">
                        <table
                            bgcolor="#ffffff"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            role="none"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p0t"
                                align="left"
                                style="
                                margin: 0;
                                background-position: center bottom;
                                background-color: transparent;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center bottom;
                                        background-color: transparent;
                                        "
                                        bgcolor="transparent"
                                        role="none"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; display: none"
                                        ></td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20b"
                                align="left"
                                style="
                                margin: 0;
                                border-radius: 30px 30px 0px 0px;
                                background-color: #515151;
                                "
                                bgcolor="#515151"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-size: 100%;
                                        background-position: left top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="logo-p-t-b"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/logo_hesed.png"
                                                alt="Foto da logomarca do Instituto Hesed"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                height="100"
                                                title="Foto da logomarca do Instituto Hesed"
                                                class="m-logo-m adapt-img"
                                                sizes="(max-width:600px) 140px, 204px"
                                            /></a>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20l es-m-p20r es-m-p40b m-bg-none"
                                align="left"
                                style="
                                margin: 0;
                                padding-top: 40px;
                                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/card_outlined_gray.jpg');
                                background-position: center top;
                                background-color: #ffffff;
                                background-repeat: no-repeat;
                                padding-right: 80px;
                                padding-left: 80px;
                                padding-bottom: 125px;
                                "
                                bgcolor="#ffffff"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 540px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            <h1
                                            style="
                                                margin: 0;
                                                line-height: 43.2px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 36px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            <strong>Redefinição de senha</strong>
                                            </h1>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            &nbsp; &nbsp;
                                            <h3
                                            style="
                                                margin: 0;
                                                line-height: 21.6px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 18px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            Querido(a) {name}.
                                            </h3>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Recebemos uma solicitação para redefinir sua senha.<br/><br/> Para criar uma nova senha, basta clicar no link abaixo:
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            ></p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Se você não fez essa solicitação, por favor, ignore este e-mail.

                                            
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Estamos à disposição para ajudar, caso precise de mais assistência!
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    style="
                                        margin: 0;
                                        padding-top: 25px;
                                        padding-bottom: 25px;
                                        font-size: 0px;
                                    "
                                    >
                                    <a
                                        href="{settings.URL_FRONTEND_CADASTRO}{url_redirect}/{token}"
                                        target="_blank"
                                        style="display: inline-block"
                                    >
                                        <img
                                        src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/btn_redefinir_senha.png"
                                        alt
                                        style="
                                            display: block;
                                            border: 0;
                                            outline: none;
                                            text-decoration: none;
                                            -ms-interpolation-mode: bicubic;
                                        "
                                        class="adapt-img"
                                        width="235"
                                        />
                                    </a>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr
                                    class="es-visible-simple-html-only"
                                    style="border-collapse: collapse"
                                >
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: separate;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        background-color: #515151;
                                        border-radius: 0 0 30px 30px;
                                        "
                                        bgcolor="#515151"
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-top: 20px"
                                        >
                                            <h2
                                            style="
                                                margin: 0;
                                                line-height: 28.8px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 24px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #ffffff;
                                            "
                                            >
                                            Instituto Hesed | Casa Mãe
                                            </h2>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="
                                            margin: 0;
                                            padding-top: 30px;
                                            padding-bottom: 40px;
                                            padding-right: 110px;
                                            padding-left: 110px;
                                            "
                                            class="es-m-p20l es-m-p20r"
                                        >
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 28px;
                                                color: #ffffff;
                                                font-size: 14px;
                                                letter-spacing: 1px;
                                            "
                                            >
                                            Av. Dionisio Leonel Alencar, 1443<br />Parque
                                            Santa Maria<br />Cep: 60873-073<br />Fortaleza
                                            – Ceará<br />(85) 3274-4513<br />contato@institutohesed.org.br
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        ></table>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </div>
        </body>
        </html>
    """
    )
    return template


def recurrence_pix_invoice_payment_email_template(
    name,
    token,
    campanha_id,
    nome_campanha,
    tipo_pagamento: Literal["pix", "invoice"],
    foto_campanha,
):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body
            style="
            height: 100%;
            width: 100%;
            font-family: roboto, 'helvetica neue', helvetica, arial, sans-serif;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            margin: 0;
            "
        >
            <div
            dir="ltr"
            class="es-wrapper-color"
            lang="pt"
            style="background-color: #ffffff"
            >
            <table
                class="es-wrapper"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                margin: 0;
                width: 100%;
                height: 100%;
                background-repeat: repeat;
                background-position: center top;
                background-image: url("https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/particula_plano_de_fundo.png");
                background-color: #ffffff;
                "
                role="none"
            >
                <tr style="border-collapse: collapse">
                <td valign="top" style="margin: 0">
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td align="center" style="margin: 0">
                        <table
                            bgcolor="#ffffff"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            role="none"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p0t"
                                align="left"
                                style="
                                margin: 0;
                                background-position: center bottom;
                                background-color: transparent;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center bottom;
                                        background-color: transparent;
                                        "
                                        bgcolor="transparent"
                                        role="none"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; display: none"
                                        ></td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20b"
                                align="left"
                                style="
                                margin: 0;
                                border-radius: 30px 30px 0px 0px;
                                background-color: #515151;
                                "
                                bgcolor="#515151"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-size: 100%;
                                        background-position: left top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="logo-p-t-b"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/logo_hesed.png"
                                                alt="Foto da Logomarca do Instituto Hesed"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                height="100"
                                                title="Foto da Logomarca do Instituto Hesed"
                                                class="m-logo-m adapt-img"
                                                sizes="(max-width:600px) 140px, 204px"
                                            /></a>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="es-m-p30b amp-banner"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="{foto_campanha}"
                                                alt="Foto da campanha que o Benfeitor realizou cadastro"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                width="374"
                                                title="Foto da campanha que o Benfeitor realizou cadastro"
                                                sizes="(max-width:600px) 80vw, 373px"
                                                class="adapt-img"
                                            /></a>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20l es-m-p20r es-m-p40b m-bg-none"
                                align="left"
                                style="
                                margin: 0;
                                padding-top: 40px;
                                background-image: url("https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/card_outline_2.jpg");
                                background-position: center top;
                                background-color: #ffffff;
                                background-repeat: no-repeat;
                                padding-right: 80px;
                                padding-left: 80px;
                                padding-bottom: 125px;
                                "
                                bgcolor="#ffffff"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 540px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            <h1
                                            style="
                                                margin: 0;
                                                line-height: 43.2px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 36px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            <strong>{nome_campanha}</strong>
                                            </h1>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            &nbsp; &nbsp;
                                            <h3
                                            style="
                                                margin: 0;
                                                line-height: 21.6px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 18px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            Querido(a) {name}.
                                            </h3>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Agradecemos por contribuir com a campanha
                                            <b>{nome_campanha}</b>
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Para facilitar sua contribuição, criamos
                                            um link seguro de pagamento que você pode
                                            acessar a qualquer momento.<br /><b
                                                >Basta clicar no botão abaixo para
                                                realizar sua doação mensal.</b
                                            >
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Agradecemos imensamente por seu comprometimento e generosidade contínuos. Se tiver alguma dúvida ou precisar de mais informações sobre nossa campanha, não hesite em nos contatar.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <b>Equipe Instituto HeSed.</b> <br/>
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Caso não seja você, por favor, desconsidere este e-mail.
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    style="
                                        margin: 0;
                                        padding-top: 25px;
                                        padding-bottom: 25px;
                                        font-size: 0px;
                                    "
                                    >
                                    <a
                                        href="{settings.URL_FRONTEND_DOE}/benfeitor/campanha/{campanha_id}/doacao?token={token}&tipo_pagamento={tipo_pagamento}"
                                        target="_blank"
                                        style="display: inline-block"
                                    >
                                        <img
                                        src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/btn_efetuar_doacao.jpg"
                                        alt
                                        style="
                                            display: block;
                                            border: 0;
                                            outline: none;
                                            text-decoration: none;
                                            -ms-interpolation-mode: bicubic;
                                        "
                                        class="adapt-img"
                                        width="235"
                                        />
                                    </a>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr
                            class="es-visible-simple-html-only"
                            style="border-collapse: collapse"
                            >
                            <td
                                align="center"
                                valign="top"
                                style="margin: 0; width: 700px"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: separate;
                                    border-spacing: 0px;
                                    background-position: center top;
                                    background-color: #515151;
                                    border-radius: 0 0 30px 30px;
                                "
                                bgcolor="#515151"
                                role="presentation"
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    style="margin: 0; padding-top: 20px"
                                    >
                                    <h2
                                        style="
                                        margin: 0;
                                        line-height: 28.8px;
                                        mso-line-height-rule: exactly;
                                        font-family: 'open sans', 'helvetica neue',
                                            helvetica, arial, sans-serif;
                                        font-size: 24px;
                                        font-style: normal;
                                        font-weight: bold;
                                        color: #ffffff;
                                        "
                                    >
                                        Instituto Hesed | Casa Mãe
                                    </h2>
                                    </td>
                                </tr>
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="left"
                                    style="
                                        margin: 0;
                                        padding-top: 30px;
                                        padding-bottom: 40px;
                                        padding-right: 110px;
                                        padding-left: 110px;
                                    "
                                    class="es-m-p20l es-m-p20r"
                                    >
                                    <p
                                        style="
                                        margin: 0;
                                        -webkit-text-size-adjust: none;
                                        -ms-text-size-adjust: none;
                                        mso-line-height-rule: exactly;
                                        font-family: roboto, 'helvetica neue',
                                            helvetica, arial, sans-serif;
                                        line-height: 28px;
                                        color: #ffffff;
                                        font-size: 14px;
                                        letter-spacing: 1px;
                                        "
                                    >
                                        Av. Dionisio Leonel Alencar, 1443 - Parque Santa
                                        Maria<br />Cep: 60873-073 | Fortaleza – Ceará<br />(85)
                                        3274-4513 - contato@institutohesed.org.br
                                    </p>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </div>
        </body>
        </html>
    """
    )
    return template


def active_account_email_template_for_emails_inactives(name, token):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body>       
            <div class="centro">
                <div class="topo">
                    <img src="https://hesedprod.blob.core.windows.net/benfeitor-public/c2c90dc1-31f4-49c2-a8fe-3f651b1b1528.png" width="200px" alt="">
                </div>
                <div class="body">
                    <h4 class="subtitle">Olá, {name}.</h4>
                    <p>Identificamos seu cadastro no Instituto Hesed, porém o cadastro encontra-se inativo.<br/><br/>
                    Caso queira ativar sua conta, clique no botão abaixo.</p>
                    <p><br/><a class="botao" href="{settings.URL_FRONTEND_CADASTRO}/?token={token}">Ativar Conta</a><br/><br/></p>
                    <p>Se você tiver alguma dúvida ou precisar de ajuda com seu login, não hesite em entrar em contato com nossa equipe de suporte ao cliente, que está disponível para ajudá-lo com qualquer problema ou preocupação.</p>
                    <p><b>Equipe Instituto HeSed.</b></p><br/>
                    <p>Caso não seja você, por favor, desconsidere este e-mail.</p>
                    <p><br/></p>
                </div>
                <div class="footer">
                    <p><b>Fale Conosco</b><br/><br/>
                    (84) 9 9123-4567 | <a href="mailto:contato@institutohesed.org.br" style="color: #FFF; text-decoration: none;">contato@institutohesed.org.br</a></p>
                </div>
            </div>
        </body>
    </html>
    """
    )
    return template


def send_cadastro_vocacional(name, url_formulario_cadastro, url_desistensia):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body>       
            <div class="centro">
                <div class="body">
                    <h4 class="subtitle">Olá, {name}.</h4>
                    <h2>Parabéns.</h1>
                    <p>
                    Temos a satisfação em comunicar que você foi aprovado para as etapas seguintes do processo de pré seleção do nosso vocacional.
                    Ao clicar no link no botão preencher cadastro você será redirecionado para preencher o nosso formulário, recomendamos que faça com algum tempo livre para não cometer equívocos no preenchimento dos dados.</p>
                    Caso queira desistie clique no botão "Escolho desistir"
                    <div class="button-wrapper">
                        <p><br/><a href="{settings.URL_FRONTEND_CADASTRO}/{url_formulario_cadastro}" class="botao">Preencher etapa</a><br/><br/></p>
                    </div>
                    <div class="button-wrapper">
                        <p><br/><a href="{settings.URL_FRONTEND_CADASTRO}/{url_desistensia}" class="botao"> Desistir do processo vocacional</a><br/><br/></p>
                    </div>
                    <p>Se você tiver alguma dúvida ou precisar de ajuda, não hesite em entrar em contato com nossa equipe de suporte ao cliente, que está disponível para ajudá-lo com qualquer problema ou preocupação.</p>
                    <p><b>Equipe Instituto HeSed.</b></p><br/>
                    <p>Caso não seja você, por favor, desconsidere este e-mail.</p>
                    <p><br/></p>
                </div>
                <div class="footer">
                    <p><b>Fale Conosco</b><br/><br/>
                    (84) 9 9123-4567 | <a href="mailto:contato@institutohesed.org.br" style="color: #FFF; text-decoration: none;">contato@institutohesed.org.br</a></p>
                </div>
            </div>
        </body>
    </html>
    """
    )
    return template


def send_cadastro_membro_oficial_aprovado(name):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body>       
            <div class="centro">
                <div class="body">
                    <h4 class="subtitle">Olá, {name}.</h4>
                    <h2>Parabéns.</h1>
                    <p>
                    Temos a satisfação em comunicar que seu cadastro como membro oficial foi aprovado. Seja bem vindo a está missão.
                    <p>Se você tiver alguma dúvida ou precisar de ajuda, não hesite em entrar em contato com nossa equipe de suporte ao cliente, que está disponível para ajudá-lo com qualquer problema ou preocupação.</p>
                    <p><b>Equipe Instituto HeSed.</b></p><br/>
                    <p>Caso não seja você, por favor, desconsidere este e-mail.</p>
                    <p><br/></p>
                </div>
                <div class="footer">
                    <p><b>Fale Conosco</b><br/><br/>
                    (84) 9 9123-4567 | <a href="mailto:contato@institutohesed.org.br" style="color: #FFF; text-decoration: none;">contato@institutohesed.org.br</a></p>
                </div>
            </div>
        </body>
    </html>
    """
    )
    return template


def send_congratulations_vocacional(name):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body>       
            <div class="centro">
                <div class="body">
                    <h4 class="subtitle">Olá, {name}.</h4>
                    <h2>Parabéns.</h1>
                    <p>
                    Temos a satisfação em comunicar que você foi aprovado no processo seleção do nosso vocacional.
                    <p>Se você tiver alguma dúvida ou precisar de ajuda, não hesite em entrar em contato com nossa equipe de suporte ao cliente, que está disponível para ajudá-lo com qualquer problema ou preocupação.</p>
                    <p><b>Equipe Instituto HeSed.</b></p><br/>
                    <p>Caso não seja você, por favor, desconsidere este e-mail.</p>
                    <p><br/></p>
                </div>
                <div class="footer">
                    <p><b>Fale Conosco</b><br/><br/>
                    (84) 9 9123-4567 | <a href="mailto:contato@institutohesed.org.br" style="color: #FFF; text-decoration: none;">contato@institutohesed.org.br</a></p>
                </div>
            </div>
        </body>
    </html>
    """
    )
    return template


def send_email_pre_cadastro_vocacional_recebido(name):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body>       
            <div class="centro">
                <div class="body">
                    <h4 class="subtitle">Olá, {name}.</h4>
                    <h2>Parabéns.</h1>
                    <p>
                    Temos a satisfação em comunicar que recebemos sua inscrição no processo vocacional, iremos analisar seu cadastro e em breve lhe daremos retorno.
                    <p>Se você tiver alguma dúvida ou precisar de ajuda, não hesite em entrar em contato com nossa equipe de suporte ao cliente, que está disponível para ajudá-lo com qualquer problema ou preocupação.</p>
                    <p><b>Equipe Instituto HeSed.</b></p><br/>
                    <p>Caso não seja você, por favor, desconsidere este e-mail.</p>
                    <p><br/></p>
                </div>
                <div class="footer">
                    <p><b>Fale Conosco</b><br/><br/>
                    (84) 9 9123-4567 | <a href="mailto:contato@institutohesed.org.br" style="color: #FFF; text-decoration: none;">contato@institutohesed.org.br</a></p>
                </div>
            </div>
        </body>
    </html>
    """
    )
    return template


def send_email_cadastro_membro_oficial_recebido(name):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body>       
            <div class="centro">
                <div class="body">
                    <h4 class="subtitle">Olá, {name}.</h4>
                    <h2>Parabéns.</h1>
                    <p>
                    Temos a satisfação em comunicar que recebemos sua inscrição para membros oficial, iremos analisar seu cadastro e em breve lhe daremos retorno.
                    <p>Se você tiver alguma dúvida ou precisar de ajuda, não hesite em entrar em contato com nossa equipe de suporte ao cliente, que está disponível para ajudá-lo com qualquer problema ou preocupação.</p>
                    <p><b>Equipe Instituto HeSed.</b></p><br/>
                    <p>Caso não seja você, por favor, desconsidere este e-mail.</p>
                    <p><br/></p>
                </div>
                <div class="footer">
                    <p><b>Fale Conosco</b><br/><br/>
                    (84) 9 9123-4567 | <a href="mailto:contato@institutohesed.org.br" style="color: #FFF; text-decoration: none;">contato@institutohesed.org.br</a></p>
                </div>
            </div>
        </body>
    </html>
    """
    )
    return template


def obrigado_pela_doacao_template(name, nome_campanha, foto_campanha):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body
            style="
            height: 100%;
            width: 100%;
            font-family: roboto, 'helvetica neue', helvetica, arial, sans-serif;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            margin: 0;
            "
        >
            <div
            dir="ltr"
            class="es-wrapper-color"
            lang="und"
            style="background-color: #ffffff"
            >
            <table
                class="es-wrapper"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                margin: 0;
                width: 100%;
                height: 100%;
                background-repeat: repeat;
                background-position: center top;
                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/particula_plano_de_fundo.png');
                background-color: #ffffff;
                "
                role="none"
            >
                <tr style="border-collapse: collapse">
                <td valign="top" style="margin: 0">
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td align="center" style="margin: 0">
                        <table
                            bgcolor="#ffffff"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            role="none"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p0t"
                                align="left"
                                style="
                                margin: 0;
                                background-position: center bottom;
                                background-color: transparent;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center bottom;
                                        background-color: transparent;
                                        "
                                        bgcolor="transparent"
                                        role="none"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; display: none"
                                        ></td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20b"
                                align="left"
                                style="
                                margin: 0;
                                border-radius: 30px 30px 0px 0px;
                                background-color: #515151;
                                "
                                bgcolor="#515151"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-size: 100%;
                                        background-position: left top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="logo-p-t-b"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/logo_hesed.png"
                                                alt="Foto da logomarca do Instituto Hesed"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                height="100"
                                                title="Foto da logomarca do Instituto Hesed"
                                                class="m-logo-m adapt-img"
                                                sizes="(max-width:600px) 140px, 204px"
                                            /></a>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="es-m-p30b amp-banner"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="{foto_campanha}"
                                                alt="Foto da campanha que o usuário realizou a doação"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                width="374"
                                                title="Foto da campanha que o usuário realizou a doação"
                                                sizes="(max-width:600px) 80vw, 373px"
                                                class="adapt-img"
                                            /></a>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20l es-m-p20r es-m-p40b m-bg-none"
                                align="left"
                                style="
                                margin: 0;
                                padding-top: 40px;
                                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/59731571905663517.jpg');
                                background-position: center top;
                                background-color: #ffffff;
                                background-repeat: no-repeat;
                                padding-right: 80px;
                                padding-left: 80px;
                                padding-bottom: 40px;
                                "
                                bgcolor="#ffffff"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 540px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            <h1
                                            style="
                                                margin: 0;
                                                line-height: 43.2px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 36px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            <strong>{nome_campanha}</strong>
                                            </h1>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            &nbsp; &nbsp;
                                            <h3
                                            style="
                                                margin: 0;
                                                line-height: 21.6px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 18px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            Querido(a) {name}.
                                            <br />Agradecemos sua generosa
                                            contribuição!
                                            </h3>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Com o coração cheio de gratidão, queremos
                                            agradecer pela sua doação ao Instituto
                                            Hesed. Seu apoio é fundamental para que
                                            possamos continuar nossa missão de
                                            promover a caridade.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Sua generosidade nos permite alcançar mais
                                            pessoas, transformar vidas e manter viva a
                                            esperança naqueles que mais precisam.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Somos profundamente gratos pela confiança
                                            depositada em nosso trabalho.
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    ></table>
                                    </td>
                                </tr>
                                <tr
                                    class="es-visible-simple-html-only"
                                    style="border-collapse: collapse"
                                >
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: separate;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        background-color: #515151;
                                        border-radius: 0 0 30px 30px;
                                        "
                                        bgcolor="#515151"
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-top: 20px"
                                        >
                                            <h2
                                            style="
                                                margin: 0;
                                                line-height: 28.8px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 24px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #ffffff;
                                            "
                                            >
                                            Instituto Hesed | Casa Mãe
                                            </h2>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="
                                            margin: 0;
                                            padding-top: 30px;
                                            padding-bottom: 40px;
                                            padding-right: 110px;
                                            padding-left: 110px;
                                            "
                                            class="es-m-p20l es-m-p20r"
                                        >
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 28px;
                                                color: #ffffff;
                                                font-size: 14px;
                                                letter-spacing: 1px;
                                            "
                                            >
                                            Av. Dionisio Leonel Alencar, 1443 - Parque
                                            Santa Maria<br />Cep: 60873-073 |
                                            Fortaleza – Ceará<br />(85) 3274-4513 -
                                            contato@institutohesed.org.br
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        ></table>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </div>
        </body>
        </html>
    """
    )
    return template


def happy_birthday_email_template(name):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body
            style="
            height: 100%;
            width: 100%;
            font-family: roboto, 'helvetica neue', helvetica, arial, sans-serif;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            margin: 0;
            "
        >
            <div
            dir="ltr"
            class="es-wrapper-color"
            lang="pt"
            style="background-color: #ffffff"
            >
            <table
                class="es-wrapper"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                margin: 0;
                width: 100%;
                height: 100%;
                background-repeat: repeat;
                background-position: center top;
                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/particula_plano_de_fundo.png');
                background-color: #ffffff;
                "
                role="none"
            >
                <tr style="border-collapse: collapse">
                <td valign="top" style="margin: 0">
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td align="center" style="margin: 0">
                        <table
                            bgcolor="#ffffff"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            role="none"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p0t"
                                align="left"
                                style="
                                margin: 0;
                                background-position: center bottom;
                                background-color: transparent;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center bottom;
                                        background-color: transparent;
                                        "
                                        bgcolor="transparent"
                                        role="none"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; display: none"
                                        ></td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20b"
                                align="left"
                                style="
                                margin: 0;
                                border-radius: 30px 30px 0px 0px;
                                background-color: #515151;
                                "
                                bgcolor="#515151"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-size: 100%;
                                        background-position: left top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="logo-p-t-b"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/logo_hesed.png"
                                                alt="Foto da logomarca do Instituto Hesed"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                height="100"
                                                title="Foto da logomarca do Instituto Hesed"
                                                class="m-logo-m adapt-img"
                                                sizes="(max-width:600px) 140px, 204px"
                                            /></a>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20l es-m-p20r es-m-p40b m-bg-none"
                                align="left"
                                style="
                                margin: 0;
                                padding-top: 40px;
                                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/card_outlined_gray.jpg');
                                background-position: center top;
                                background-color: #ffffff;
                                background-repeat: no-repeat;
                                padding-right: 80px;
                                padding-left: 80px;
                                padding-bottom: 125px;
                                "
                                bgcolor="#ffffff"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 540px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            <h1
                                            style="
                                                margin: 0;
                                                line-height: 43.2px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 36px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            <strong>Feliz Aniversário!</strong>
                                            </h1>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            &nbsp; &nbsp;
                                            <h3
                                            style="
                                                margin: 0;
                                                line-height: 21.6px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 18px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            Querido(a) {name}.
                                            </h3>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Hoje é um dia muito especial, e queremos
                                            celebrar com você! Que seu aniversário
                                            seja repleto de alegria, paz e bênçãos.
                                            Que Deus continue iluminando seu caminho,
                                            guiando seus passos e abençoando sua vida
                                            com saúde, amor e prosperidade.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            ></p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Agradecemos por fazer parte da nossa
                                            comunidade no Instituto Hesed, e esperamos
                                            que este novo ano seja cheio de
                                            realizações e momentos felizes.<br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Parabéns e muitas felicidades!
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr
                                    class="es-visible-simple-html-only"
                                    style="border-collapse: collapse"
                                >
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: separate;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        background-color: #515151;
                                        border-radius: 0 0 30px 30px;
                                        "
                                        bgcolor="#515151"
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-top: 20px"
                                        >
                                            <h2
                                            style="
                                                margin: 0;
                                                line-height: 28.8px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 24px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #ffffff;
                                            "
                                            >
                                            Instituto Hesed | Casa Mãe
                                            </h2>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="
                                            margin: 0;
                                            padding-top: 30px;
                                            padding-bottom: 40px;
                                            padding-right: 110px;
                                            padding-left: 110px;
                                            "
                                            class="es-m-p20l es-m-p20r"
                                        >
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 28px;
                                                color: #ffffff;
                                                font-size: 14px;
                                                letter-spacing: 1px;
                                            "
                                            >
                                            Av. Dionisio Leonel Alencar, 1443<br />Parque
                                            Santa Maria<br />Cep: 60873-073<br />Fortaleza
                                            – Ceará<br />(85) 3274-4513<br />contato@institutohesed.org.br
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        ></table>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </div>
        </body>
        </html>
    """
    )
    return template


def delete_account_message_email_template(name):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body
            style="
            height: 100%;
            width: 100%;
            font-family: roboto, 'helvetica neue', helvetica, arial, sans-serif;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            margin: 0;
            "
        >
            <div
            dir="ltr"
            class="es-wrapper-color"
            lang="pt"
            style="background-color: #ffffff"
            >
            <table
                class="es-wrapper"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                margin: 0;
                width: 100%;
                height: 100%;
                background-repeat: repeat;
                background-position: center top;
                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/particula_plano_de_fundo.png');
                background-color: #ffffff;
                "
                role="none"
            >
                <tr style="border-collapse: collapse">
                <td valign="top" style="margin: 0">
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td align="center" style="margin: 0">
                        <table
                            bgcolor="#ffffff"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            role="none"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p0t"
                                align="left"
                                style="
                                margin: 0;
                                background-position: center bottom;
                                background-color: transparent;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center bottom;
                                        background-color: transparent;
                                        "
                                        bgcolor="transparent"
                                        role="none"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; display: none"
                                        ></td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20b"
                                align="left"
                                style="
                                margin: 0;
                                border-radius: 30px 30px 0px 0px;
                                background-color: #515151;
                                "
                                bgcolor="#515151"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-size: 100%;
                                        background-position: left top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="logo-p-t-b"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/logo_hesed.png"
                                                alt="Foto da logomarca do Instituto Hesed"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                height="100"
                                                title="Foto da logomarca do Instituto Hesed"
                                                class="m-logo-m adapt-img"
                                                sizes="(max-width:600px) 140px, 204px"
                                            /></a>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20l es-m-p20r es-m-p40b m-bg-none"
                                align="left"
                                style="
                                margin: 0;
                                padding-top: 40px;
                                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/card_outlined_gray.jpg');
                                background-position: center top;
                                background-color: #ffffff;
                                background-repeat: no-repeat;
                                padding-right: 80px;
                                padding-left: 80px;
                                padding-bottom: 125px;
                                "
                                bgcolor="#ffffff"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 540px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            <h1
                                            style="
                                                margin: 0;
                                                line-height: 43.2px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 36px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            <strong>Confirmação de Exclusão de Cadastro</strong>
                                            </h1>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            &nbsp; &nbsp;
                                            <h3
                                            style="
                                                margin: 0;
                                                line-height: 12px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 18px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            Querido(a) {name}.
                                            </h3>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Conforme sua solicitação, informamos que seu cadastro foi excluído com sucesso do nosso sistema.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            ></p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Lamentamos sua saída, mas respeitamos sua decisão. Se, no futuro, decidir se juntar novamente à nossa comunidade, estaremos de portas abertas para recebê-lo(a).
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Agradecemos pela sua participação e desejamos muitas bênçãos em sua jornada!
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr
                                    class="es-visible-simple-html-only"
                                    style="border-collapse: collapse"
                                >
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: separate;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        background-color: #515151;
                                        border-radius: 0 0 30px 30px;
                                        "
                                        bgcolor="#515151"
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-top: 20px"
                                        >
                                            <h2
                                            style="
                                                margin: 0;
                                                line-height: 28.8px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 24px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #ffffff;
                                            "
                                            >
                                            Instituto Hesed | Casa Mãe
                                            </h2>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="
                                            margin: 0;
                                            padding-top: 30px;
                                            padding-bottom: 40px;
                                            padding-right: 110px;
                                            padding-left: 110px;
                                            "
                                            class="es-m-p20l es-m-p20r"
                                        >
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 28px;
                                                color: #ffffff;
                                                font-size: 14px;
                                                letter-spacing: 1px;
                                            "
                                            >
                                            Av. Dionisio Leonel Alencar, 1443<br />Parque
                                            Santa Maria<br />Cep: 60873-073<br />Fortaleza
                                            – Ceará<br />(85) 3274-4513<br />contato@institutohesed.org.br
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        ></table>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </div>
        </body>
        </html>
    """
    )
    return template


def update_register_email_template(name):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body
            style="
            height: 100%;
            width: 100%;
            font-family: roboto, 'helvetica neue', helvetica, arial, sans-serif;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            margin: 0;
            "
        >
            <div
            dir="ltr"
            class="es-wrapper-color"
            lang="pt"
            style="background-color: #ffffff"
            >
            <table
                class="es-wrapper"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                margin: 0;
                width: 100%;
                height: 100%;
                background-repeat: repeat;
                background-position: center top;
                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/particula_plano_de_fundo.png');
                background-color: #ffffff;
                "
                role="none"
            >
                <tr style="border-collapse: collapse">
                <td valign="top" style="margin: 0">
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td align="center" style="margin: 0">
                        <table
                            bgcolor="#ffffff"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            role="none"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p0t"
                                align="left"
                                style="
                                margin: 0;
                                background-position: center bottom;
                                background-color: transparent;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center bottom;
                                        background-color: transparent;
                                        "
                                        bgcolor="transparent"
                                        role="none"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; display: none"
                                        ></td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20b"
                                align="left"
                                style="
                                margin: 0;
                                border-radius: 30px 30px 0px 0px;
                                background-color: #515151;
                                "
                                bgcolor="#515151"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-size: 100%;
                                        background-position: left top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="logo-p-t-b"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/logo_hesed.png"
                                                alt="Foto da logomarca do Instituto Hesed"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                height="100"
                                                title="Foto da logomarca do Instituto Hesed"
                                                class="m-logo-m adapt-img"
                                                sizes="(max-width:600px) 140px, 204px"
                                            /></a>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20l es-m-p20r es-m-p40b m-bg-none"
                                align="left"
                                style="
                                margin: 0;
                                padding-top: 40px;
                                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/card_outlined_gray.jpg');
                                background-position: center top;
                                background-color: #ffffff;
                                background-repeat: no-repeat;
                                padding-right: 80px;
                                padding-left: 80px;
                                padding-bottom: 125px;
                                "
                                bgcolor="#ffffff"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 540px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            <h1
                                            style="
                                                margin: 0;
                                                line-height: 43.2px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 36px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            <strong>Atualize seu cadastro</strong>
                                            </h1>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            &nbsp; &nbsp;
                                            <h3
                                            style="
                                                margin: 0;
                                                line-height: 21.6px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 18px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            Querido(a) {name}.
                                            </h3>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Temos uma novidade! Estamos de plataforma
                                            nova e queremos garantir que seu cadastro
                                            esteja sempre atualizado. Agora, além de
                                            atualizar suas informações, você também
                                            poderá adicionar uma foto ao seu perfil,
                                            tornando sua experiência ainda mais
                                            personalizada.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            ></p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Acesse o link abaixo para revisar e
                                            atualizar seus dados cadastrais:
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Sua colaboração é muito importante para
                                            que possamos continuar oferecendo o melhor
                                            atendimento. Se precisar de ajuda, estamos
                                            à disposição! <br/> Agradecemos sua atenção e
                                            contamos com sua participação!
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    style="
                                        margin: 0;
                                        padding-top: 25px;
                                        padding-bottom: 25px;
                                        font-size: 0px;
                                    "
                                    >
                                    <a
                                        href="https://doe.institutohesed.org.br/"
                                        target="_blank"
                                        style="display: inline-block"
                                    >
                                        <img
                                        src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/btn_atualizar_cadastro.png"
                                        alt
                                        style="
                                            display: block;
                                            border: 0;
                                            outline: none;
                                            text-decoration: none;
                                            -ms-interpolation-mode: bicubic;
                                        "
                                        class="adapt-img"
                                        width="235"
                                        />
                                    </a>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr
                                    class="es-visible-simple-html-only"
                                    style="border-collapse: collapse"
                                >
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: separate;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        background-color: #515151;
                                        border-radius: 0 0 30px 30px;
                                        "
                                        bgcolor="#515151"
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-top: 20px"
                                        >
                                            <h2
                                            style="
                                                margin: 0;
                                                line-height: 28.8px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 24px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #ffffff;
                                            "
                                            >
                                            Instituto Hesed | Casa Mãe
                                            </h2>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="
                                            margin: 0;
                                            padding-top: 30px;
                                            padding-bottom: 40px;
                                            padding-right: 110px;
                                            padding-left: 110px;
                                            "
                                            class="es-m-p20l es-m-p20r"
                                        >
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 28px;
                                                color: #ffffff;
                                                font-size: 14px;
                                                letter-spacing: 1px;
                                            "
                                            >
                                            Av. Dionisio Leonel Alencar, 1443<br />Parque
                                            Santa Maria<br />Cep: 60873-073<br />Fortaleza
                                            – Ceará<br />(85) 3274-4513<br />contato@institutohesed.org.br
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        ></table>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </div>
        </body>
        </html>
    """
    )
    return template


def reminder_recurrence_donation_email_template(
    nome_benfeitor,
    campanha_id,
    nome_campanha,
    foto_campanha,
    tipo_pagamento: Literal["pix", "invoice"],
    metodo_pagamento,
    data_vencimento,
    token,
):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body
            style="
            height: 100%;
            width: 100%;
            font-family: roboto, 'helvetica neue', helvetica, arial, sans-serif;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            margin: 0;
            "
        >
            <div
            dir="ltr"
            class="es-wrapper-color"
            lang="pt"
            style="background-color: #ffffff"
            >
            <table
                class="es-wrapper"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                margin: 0;
                width: 100%;
                height: 100%;
                background-repeat: repeat;
                background-position: center top;
                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/particula_plano_de_fundo.png');
                background-color: #ffffff;
                "
                role="none"
            >
                <tr style="border-collapse: collapse">
                <td valign="top" style="margin: 0">
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td align="center" style="margin: 0">
                        <table
                            bgcolor="#ffffff"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            role="none"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p0t"
                                align="left"
                                style="
                                margin: 0;
                                background-position: center bottom;
                                background-color: transparent;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center bottom;
                                        background-color: transparent;
                                        "
                                        bgcolor="transparent"
                                        role="none"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; display: none"
                                        ></td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20b"
                                align="left"
                                style="
                                margin: 0;
                                border-radius: 30px 30px 0px 0px;
                                background-color: #515151;
                                "
                                bgcolor="#515151"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-size: 100%;
                                        background-position: left top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="logo-p-t-b"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/logo_hesed.png"
                                                alt="Foto da Logomarca do Instituto Hesed"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                height="100"
                                                title="Foto da Logomarca do Instituto Hesed"
                                                class="m-logo-m adapt-img"
                                                sizes="(max-width:600px) 140px, 204px"
                                            /></a>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="es-m-p30b amp-banner"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="{foto_campanha}"
                                                alt="Foto da campanha que o Benfeitor realizou cadastro"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                width="374"
                                                title="Foto da campanha que o Benfeitor realizou cadastro"
                                                sizes="(max-width:600px) 80vw, 373px"
                                                class="adapt-img"
                                            /></a>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20l es-m-p20r es-m-p40b m-bg-none"
                                align="left"
                                style="
                                margin: 0;
                                padding-top: 40px;
                                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/card_outline_2.jpg');
                                background-position: center top;
                                background-color: #ffffff;
                                background-repeat: no-repeat;
                                padding-right: 80px;
                                padding-left: 80px;
                                padding-bottom: 125px;
                                "
                                bgcolor="#ffffff"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 540px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            <h1
                                            style="
                                                margin: 0;
                                                line-height: 43.2px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 36px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            <strong>{nome_campanha}</strong>
                                            </h1>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            &nbsp; &nbsp;
                                            <h3
                                            style="
                                                margin: 0;
                                                line-height: 21.6px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 18px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            Querido(a) {nome_benfeitor}.
                                            </h3>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Sua doação recorrente está se aproximando
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Esperamos que você esteja bem! Estamos
                                            enviando este lembrete para avisar que sua
                                            doação recorrente para o Instituto Hesed
                                            está prevista para os próximos dias.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Sua contribuição mensal é essencial para
                                            que possamos continuar com nossa missão de
                                            de promover a caridade. Agradecemos
                                            imensamente pelo seu apoio e generosidade,
                                            que fazem uma diferença significativa em
                                            nossas ações e no atendimento àqueles que
                                            mais precisam.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Se você fez a opção de doação via {metodo_pagamento}, lembre-se de efetuar o pagamento
                                            até o dia {data_vencimento}. Caso tenha alguma dúvida
                                            ou precise de assistência, estamos à
                                            disposição!
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Que Deus abençoe você e sua generosidade!
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    style="
                                        margin: 0;
                                        padding-top: 25px;
                                        padding-bottom: 25px;
                                        font-size: 0px;
                                    "
                                    >
                                    <a
                                        href="{settings.URL_FRONTEND_DOE}/benfeitor/campanha/{campanha_id}/doacao?token={token}&tipo_pagamento={tipo_pagamento}"
                                        target="_blank"
                                        style="display: inline-block"
                                    >
                                        <img
                                        src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/btn_efetuar_doacao.jpg"
                                        alt
                                        style="
                                            display: block;
                                            border: 0;
                                            outline: none;
                                            text-decoration: none;
                                            -ms-interpolation-mode: bicubic;
                                        "
                                        class="adapt-img"
                                        width="235"
                                        />
                                    </a>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr
                            class="es-visible-simple-html-only"
                            style="border-collapse: collapse"
                            >
                            <td
                                align="center"
                                valign="top"
                                style="margin: 0; width: 700px"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: separate;
                                    border-spacing: 0px;
                                    background-position: center top;
                                    background-color: #515151;
                                    border-radius: 0 0 30px 30px;
                                "
                                bgcolor="#515151"
                                role="presentation"
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    style="margin: 0; padding-top: 20px"
                                    >
                                    <h2
                                        style="
                                        margin: 0;
                                        line-height: 28.8px;
                                        mso-line-height-rule: exactly;
                                        font-family: 'open sans', 'helvetica neue',
                                            helvetica, arial, sans-serif;
                                        font-size: 24px;
                                        font-style: normal;
                                        font-weight: bold;
                                        color: #ffffff;
                                        "
                                    >
                                        Instituto Hesed | Casa Mãe
                                    </h2>
                                    </td>
                                </tr>
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="left"
                                    style="
                                        margin: 0;
                                        padding-top: 30px;
                                        padding-bottom: 40px;
                                        padding-right: 110px;
                                        padding-left: 110px;
                                    "
                                    class="es-m-p20l es-m-p20r"
                                    >
                                    <p
                                        style="
                                        margin: 0;
                                        -webkit-text-size-adjust: none;
                                        -ms-text-size-adjust: none;
                                        mso-line-height-rule: exactly;
                                        font-family: roboto, 'helvetica neue',
                                            helvetica, arial, sans-serif;
                                        line-height: 28px;
                                        color: #ffffff;
                                        font-size: 14px;
                                        letter-spacing: 1px;
                                        "
                                    >
                                        Av. Dionisio Leonel Alencar, 1443 - Parque Santa
                                        Maria<br />Cep: 60873-073 | Fortaleza – Ceará<br />(85)
                                        3274-4513 - contato@institutohesed.org.br
                                    </p>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </div>
        </body>
        </html>
    """
    )
    return template


def reminder_unpaid_donation_email_template(
    nome_benfeitor,
    campanha_id,
    nome_campanha,
    foto_campanha,
    tipo_pagamento: Literal["pix", "invoice"],
    data_vencimento,
    token,
):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body
            style="
            height: 100%;
            width: 100%;
            font-family: roboto, 'helvetica neue', helvetica, arial, sans-serif;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            margin: 0;
            "
        >
            <div
            dir="ltr"
            class="es-wrapper-color"
            lang="pt"
            style="background-color: #ffffff"
            >
            <table
                class="es-wrapper"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                margin: 0;
                width: 100%;
                height: 100%;
                background-repeat: repeat;
                background-position: center top;
                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/particula_plano_de_fundo.png');
                background-color: #ffffff;
                "
                role="none"
            >
                <tr style="border-collapse: collapse">
                <td valign="top" style="margin: 0">
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td align="center" style="margin: 0">
                        <table
                            bgcolor="#ffffff"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            role="none"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p0t"
                                align="left"
                                style="
                                margin: 0;
                                background-position: center bottom;
                                background-color: transparent;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center bottom;
                                        background-color: transparent;
                                        "
                                        bgcolor="transparent"
                                        role="none"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; display: none"
                                        ></td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20b"
                                align="left"
                                style="
                                margin: 0;
                                border-radius: 30px 30px 0px 0px;
                                background-color: #515151;
                                "
                                bgcolor="#515151"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-size: 100%;
                                        background-position: left top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="logo-p-t-b"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/logo_hesed.png"
                                                alt="Foto da Logomarca do Instituto Hesed"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                height="100"
                                                title="Foto da Logomarca do Instituto Hesed"
                                                class="m-logo-m adapt-img"
                                                sizes="(max-width:600px) 140px, 204px"
                                            /></a>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="es-m-p30b amp-banner"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="{foto_campanha}"
                                                alt="Foto da campanha que o Benfeitor realizou cadastro"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                width="374"
                                                title="Foto da campanha que o Benfeitor realizou cadastro"
                                                sizes="(max-width:600px) 80vw, 373px"
                                                class="adapt-img"
                                            /></a>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20l es-m-p20r es-m-p40b m-bg-none"
                                align="left"
                                style="
                                margin: 0;
                                padding-top: 40px;
                                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/card_outline_2.jpg');
                                background-position: center top;
                                background-color: #ffffff;
                                background-repeat: no-repeat;
                                padding-right: 80px;
                                padding-left: 80px;
                                padding-bottom: 125px;
                                "
                                bgcolor="#ffffff"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 540px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            <h1
                                            style="
                                                margin: 0;
                                                line-height: 43.2px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 36px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            <strong>{nome_campanha}</strong>
                                            </h1>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            &nbsp; &nbsp;
                                            <h3
                                            style="
                                                margin: 0;
                                                line-height: 21.6px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 18px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            Querido(a) {nome_benfeitor}.
                                            </h3>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Esperamos que você esteja bem!
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Notamos que a sua doação recorrente,
                                            prevista para o dia {data_vencimento}, ainda não foi
                                            confirmada. Sabemos que imprevistos podem
                                            acontecer, por isso estamos enviando este
                                            lembrete.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Sua generosidade é fundamental para que possamos continuar com nossa missão de promover a caridade, e contamos com o seu apoio. Se possível, pedimos gentilmente que regularize sua doação para que possamos seguir juntos transformando vidas.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                        <br/>
                                            Caso tenha ocorrido algum problema ou precise de assistência, estamos aqui para ajudar!
                                            Agradecemos sua atenção e que Deus abençoe sua generosidade!
                                            </p>
                                        
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    style="
                                        margin: 0;
                                        padding-top: 25px;
                                        padding-bottom: 25px;
                                        font-size: 0px;
                                    "
                                    >
                                    <a
                                        href="{settings.URL_FRONTEND_DOE}/benfeitor/campanha/{campanha_id}/doacao?token={token}&tipo_pagamento={tipo_pagamento}"
                                        target="_blank"
                                        style="display: inline-block"
                                    >
                                        <img
                                        src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/btn_efetuar_doacao.jpg"
                                        alt
                                        style="
                                            display: block;
                                            border: 0;
                                            outline: none;
                                            text-decoration: none;
                                            -ms-interpolation-mode: bicubic;
                                        "
                                        class="adapt-img"
                                        width="235"
                                        />
                                    </a>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr
                            class="es-visible-simple-html-only"
                            style="border-collapse: collapse"
                            >
                            <td
                                align="center"
                                valign="top"
                                style="margin: 0; width: 700px"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: separate;
                                    border-spacing: 0px;
                                    background-position: center top;
                                    background-color: #515151;
                                    border-radius: 0 0 30px 30px;
                                "
                                bgcolor="#515151"
                                role="presentation"
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    style="margin: 0; padding-top: 20px"
                                    >
                                    <h2
                                        style="
                                        margin: 0;
                                        line-height: 28.8px;
                                        mso-line-height-rule: exactly;
                                        font-family: 'open sans', 'helvetica neue',
                                            helvetica, arial, sans-serif;
                                        font-size: 24px;
                                        font-style: normal;
                                        font-weight: bold;
                                        color: #ffffff;
                                        "
                                    >
                                        Instituto Hesed | Casa Mãe
                                    </h2>
                                    </td>
                                </tr>
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="left"
                                    style="
                                        margin: 0;
                                        padding-top: 30px;
                                        padding-bottom: 40px;
                                        padding-right: 110px;
                                        padding-left: 110px;
                                    "
                                    class="es-m-p20l es-m-p20r"
                                    >
                                    <p
                                        style="
                                        margin: 0;
                                        -webkit-text-size-adjust: none;
                                        -ms-text-size-adjust: none;
                                        mso-line-height-rule: exactly;
                                        font-family: roboto, 'helvetica neue',
                                            helvetica, arial, sans-serif;
                                        line-height: 28px;
                                        color: #ffffff;
                                        font-size: 14px;
                                        letter-spacing: 1px;
                                        "
                                    >
                                        Av. Dionisio Leonel Alencar, 1443 - Parque Santa
                                        Maria<br />Cep: 60873-073 | Fortaleza – Ceará<br />(85)
                                        3274-4513 - contato@institutohesed.org.br
                                    </p>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </div>
        </body>
        </html>
    """
    )
    return template


def active_account_alistamento_email_template(nome: str, token: str):
    template = (
        TEMPLATE_HEAD
        + f"""
        <body
            style="
            height: 100%;
            width: 100%;
            font-family: roboto, 'helvetica neue', helvetica, arial, sans-serif;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            margin: 0;
            "
        >
            <div
            dir="ltr"
            class="es-wrapper-color"
            lang="pt"
            style="background-color: #ffffff"
            >
            <table
                class="es-wrapper"
                width="100%"
                cellspacing="0"
                cellpadding="0"
                style="
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
                border-collapse: collapse;
                border-spacing: 0px;
                margin: 0;
                width: 100%;
                height: 100%;
                background-repeat: repeat;
                background-position: center top;
                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/particula_plano_de_fundo.png');
                background-color: #ffffff;
                "
                role="none"
            >
                <tr style="border-collapse: collapse">
                <td valign="top" style="margin: 0">
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td align="center" style="margin: 0">
                        <table
                            bgcolor="#ffffff"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            role="none"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p0t"
                                align="left"
                                style="
                                margin: 0;
                                background-position: center bottom;
                                background-color: transparent;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center bottom;
                                        background-color: transparent;
                                        "
                                        bgcolor="transparent"
                                        role="none"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; display: none"
                                        ></td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    >
                    <tr style="border-collapse: collapse">
                        <td
                        align="center"
                        bgcolor="transparent"
                        style="margin: 0; background-color: transparent"
                        >
                        <table
                            bgcolor="transparent"
                            class="es-content-body"
                            align="center"
                            cellpadding="0"
                            cellspacing="0"
                            style="
                            mso-table-lspace: 0pt;
                            mso-table-rspace: 0pt;
                            border-collapse: collapse;
                            border-spacing: 0px;
                            background-color: transparent;
                            width: 700px;
                            "
                            role="none"
                        >
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20b"
                                align="left"
                                style="
                                margin: 0;
                                border-radius: 30px 30px 0px 0px;
                                background-color: #515151;
                                "
                                bgcolor="#515151"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-size: 100%;
                                        background-position: left top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="logo-p-t-b"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/logo_hesed.png"
                                                alt="Foto da Logomarca do Instituto Hesed"
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                height="100"
                                                title="Foto da Logomarca do Instituto Hesed"
                                                class="m-logo-m adapt-img"
                                                sizes="(max-width:600px) 140px, 204px"
                                            /></a>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            class="es-m-p30b amp-banner"
                                            style="margin: 0; font-size: 0px"
                                        >
                                            <a
                                            target="_blank"
                                            href="https://institutohesed.org.br/"
                                            style="
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                text-decoration: underline;
                                                color: #000001;
                                                font-size: 15px;
                                            "
                                            ><img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/bg_bible.jpg"
                                                alt
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                sizes="(max-width:600px) 80vw, 373px"
                                                class="adapt-img"
                                                width="700"
                                            /></a>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="es-m-p20l es-m-p20r es-m-p40b m-bg-none"
                                align="left"
                                style="
                                margin: 0;
                                padding-top: 40px;
                                background-image: url('https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/card_outline.jpg');
                                background-position: center top;
                                background-color: #ffffff;
                                background-repeat: no-repeat;
                                padding-right: 80px;
                                padding-left: 80px;
                                padding-bottom: 125px;
                                "
                                bgcolor="#ffffff"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 540px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            <h1
                                            style="
                                                margin: 0;
                                                line-height: 43.2px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 36px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            <strong>Seja bem vindo(a)</strong>
                                            </h1>
                                        </td>
                                        </tr>
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="left"
                                            style="margin: 0; padding-bottom: 10px"
                                        >
                                            &nbsp; &nbsp;
                                            <h3
                                            style="
                                                margin: 0;
                                                line-height: 21.6px;
                                                mso-line-height-rule: exactly;
                                                font-family: 'open sans',
                                                'helvetica neue', helvetica, arial,
                                                sans-serif;
                                                font-size: 18px;
                                                font-style: normal;
                                                font-weight: bold;
                                                color: #000000;
                                            "
                                            >
                                            Querido(a) {nome}.
                                            </h3>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            É com grande alegria que te damos as
                                            boas-vindas!
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Estamos muito felizes em tê-lo(a) conosco
                                            e agradecemos por se juntar à nossa missão
                                            de promover a caridade e os valores
                                            cristãos em nossa comunidade.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            A partir de agora, você estará
                                            conectado(a) a tudo o que fazemos,
                                            recebendo informações e oportunidades para
                                            participar ativamente em nossa comunidade
                                            e ações.
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            <br />
                                            </p>
                                            <p
                                            style="
                                                margin: 0;
                                                -webkit-text-size-adjust: none;
                                                -ms-text-size-adjust: none;
                                                mso-line-height-rule: exactly;
                                                font-family: roboto, 'helvetica neue',
                                                helvetica, arial, sans-serif;
                                                line-height: 30px;
                                                color: #000000;
                                                font-size: 15px;
                                            "
                                            >
                                            Que esta nova caminhada seja abençoada e
                                            repleta de realizações. Estamos aqui para
                                            apoiar e caminhar junto com você!
                                            </p>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr style="border-collapse: collapse">
                            <td
                                class="m-bg-auto"
                                align="left"
                                style="
                                margin: 0;
                                background-size: 100% 100%;
                                background-color: transparent;
                                background-position: center top;
                                "
                                bgcolor="transparent"
                            >
                                <table
                                cellpadding="0"
                                cellspacing="0"
                                width="100%"
                                role="none"
                                style="
                                    mso-table-lspace: 0pt;
                                    mso-table-rspace: 0pt;
                                    border-collapse: collapse;
                                    border-spacing: 0px;
                                "
                                >
                                <tr style="border-collapse: collapse">
                                    <td
                                    align="center"
                                    valign="top"
                                    style="margin: 0; width: 700px"
                                    >
                                    <table
                                        cellpadding="0"
                                        cellspacing="0"
                                        width="100%"
                                        style="
                                        mso-table-lspace: 0pt;
                                        mso-table-rspace: 0pt;
                                        border-collapse: collapse;
                                        border-spacing: 0px;
                                        background-position: center top;
                                        "
                                        role="presentation"
                                    >
                                        <tr style="border-collapse: collapse">
                                        <td
                                            align="center"
                                            style="
                                            margin: 0;
                                            padding-top: 25px;
                                            padding-bottom: 25px;
                                            font-size: 0px;
                                            "
                                        >
                                            <a
                                            href="https://cadastro.institutohesed.org.br/membro-exercito/landing-page-membros?alistamento_esm_token={token}"
                                            target="_blank"
                                            style="display: inline-block"
                                            >
                                            <img
                                                src="https://hesed-bucket.s3.sa-east-1.amazonaws.com/templates_email/btn_concluir_cadastro.jpg"
                                                alt=""
                                                style="
                                                display: block;
                                                border: 0;
                                                outline: none;
                                                text-decoration: none;
                                                -ms-interpolation-mode: bicubic;
                                                "
                                                class="adapt-img"
                                                width="250"
                                            />
                                            </a>
                                        </td>
                                        </tr>
                                        <tr
                                        class="es-visible-simple-html-only"
                                        style="border-collapse: collapse"
                                        >
                                        <td
                                            align="center"
                                            valign="top"
                                            style="margin: 0; width: 700px"
                                        >
                                            <table
                                            cellpadding="0"
                                            cellspacing="0"
                                            width="100%"
                                            style="
                                                mso-table-lspace: 0pt;
                                                mso-table-rspace: 0pt;
                                                border-collapse: separate;
                                                border-spacing: 0px;
                                                background-position: center top;
                                                background-color: #515151;
                                                border-radius: 0 0 30px 30px;
                                            "
                                            bgcolor="#515151"
                                            role="presentation"
                                            >
                                            <tr style="border-collapse: collapse">
                                                <td
                                                align="center"
                                                style="margin: 0; padding-top: 20px"
                                                >
                                                <h2
                                                    style="
                                                    margin: 0;
                                                    line-height: 28.8px;
                                                    mso-line-height-rule: exactly;
                                                    font-family: 'open sans',
                                                        'helvetica neue', helvetica,
                                                        arial, sans-serif;
                                                    font-size: 24px;
                                                    font-style: normal;
                                                    font-weight: bold;
                                                    color: #ffffff;
                                                    "
                                                >
                                                    Instituto Hesed | Casa Mãe
                                                </h2>
                                                </td>
                                            </tr>
                                            <tr style="border-collapse: collapse">
                                                <td
                                                align="left"
                                                style="
                                                    margin: 0;
                                                    padding-top: 30px;
                                                    padding-bottom: 40px;
                                                    padding-right: 110px;
                                                    padding-left: 110px;
                                                "
                                                class="es-m-p20l es-m-p20r"
                                                >
                                                <p
                                                    style="
                                                    margin: 0;
                                                    -webkit-text-size-adjust: none;
                                                    -ms-text-size-adjust: none;
                                                    mso-line-height-rule: exactly;
                                                    font-family: roboto,
                                                        'helvetica neue', helvetica,
                                                        arial, sans-serif;
                                                    line-height: 28px;
                                                    color: #ffffff;
                                                    font-size: 14px;
                                                    letter-spacing: 1px;
                                                    "
                                                >
                                                    Av. Dionisio Leonel Alencar, 1443 -
                                                    Parque Santa Maria<br />Cep:
                                                    60873-073 | Fortaleza – Ceará<br />(85)
                                                    3274-4513 -
                                                    contato@institutohesed.org.br
                                                </p>
                                                </td>
                                            </tr>
                                            </table>
                                        </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                    <table
                    cellpadding="0"
                    cellspacing="0"
                    class="es-content"
                    align="center"
                    role="none"
                    style="
                        mso-table-lspace: 0pt;
                        mso-table-rspace: 0pt;
                        border-collapse: collapse;
                        border-spacing: 0px;
                        table-layout: fixed !important;
                        width: 100%;
                    "
                    ></table>
                </td>
                </tr>
            </table>
            </div>
        </body>
        </html>
    """
    )
    return template

from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

from src.managers.commands import ExchangeCommandMgr, PromoCommandMgr, QuestsCommandMgr, \
    RegisterCommandMgr, ReusableComponents, WalletClaimCommandMgr
from src.managers.commands.BroadcastCommand import BroadcastCommandMgr, BroadcastMessageMgr, BroadcastPhotoMgr


def get_registration_states():
    states = {
        'NewUserEmail': [
            MessageHandler(Filters.text, RegisterCommandMgr.new_user_email)
        ],

        'NewUserGender': [
            MessageHandler(Filters.text, RegisterCommandMgr.new_user_gender)
        ],

        'NewUserReferralSkip': [
            MessageHandler(
                Filters.text, RegisterCommandMgr.new_user_referral_skip)
        ],

        'NewUserReferralInput': [
            MessageHandler(
                Filters.text, RegisterCommandMgr.new_user_referral_input)
        ]
    }

    return states


def get_reg_fallback_handlers():
    handlers = [
        CommandHandler('cancel', RegisterCommandMgr.cancel_registration),

        CommandHandler(
            'skip', RegisterCommandMgr.new_user_referral_skip_warning)
    ]

    return handlers


def get_promo_code_states():
    states = {
        'PromoCodeInput': [
            MessageHandler(Filters.text, PromoCommandMgr.promo_code_input)
        ],

        ConversationHandler.TIMEOUT: [
            MessageHandler(Filters.all, ReusableComponents.timeout_handler)
        ]
    }

    return states


def get_exchange_states():
    states = {
        'ExchangeInput': [
            MessageHandler(Filters.text, ExchangeCommandMgr.exchange_input)
        ],

        ConversationHandler.TIMEOUT: [
            MessageHandler(Filters.all, ReusableComponents.timeout_handler)
        ]
    }

    return states


def get_wallet_states():
    states = {
        'ViewVoucher': [
            MessageHandler(
                Filters.text, WalletClaimCommandMgr.view_selected_voucher)
        ],

        'ClaimVoucher': [
            MessageHandler(Filters.text, WalletClaimCommandMgr.claim_voucher)
        ],

        ConversationHandler.TIMEOUT: [
            MessageHandler(Filters.all, ReusableComponents.timeout_handler)
        ]
    }

    return states


def get_mass_broadcast_states():
    states = {
        'SendOption': [
            MessageHandler(Filters.text, BroadcastCommandMgr.broadcast_choice)
        ],

        'SendMessage': [
            MessageHandler(
                Filters.text, BroadcastMessageMgr.broadcast_message)
        ],

        'AskCaption': [
            MessageHandler(
                Filters.photo, BroadcastPhotoMgr.prompt_photo_caption)
        ],

        'CaptionChoice': [
            MessageHandler(
                Filters.text, BroadcastPhotoMgr.input_photo_caption)
        ],

        'SendPhoto': [
            MessageHandler(
                Filters.text, BroadcastPhotoMgr.broadcast_photo)
        ]
    }

    return states


def get_quest_states():
    states = {
        'QuestDescription': [
            MessageHandler(
                Filters.text, QuestsCommandMgr.display_quest_description)
        ],

        'ImageResponse': [
            MessageHandler(
                Filters.photo, QuestsCommandMgr.after_send_quest_image)
        ],

        ConversationHandler.TIMEOUT: [
            MessageHandler(Filters.all, ReusableComponents.timeout_handler)
        ]
    }

    return states


def get_fallback_handler():
    handler = [
        CommandHandler('cancel', ReusableComponents.cancel_current_action)
    ]

    return handler

from telegram.ext import CommandHandler, ConversationHandler

from src.managers import StateManager
from src.managers.commands import ExchangeCommandMgr, PromoCommandMgr, QuestsCommandMgr, \
    ReferralCodeCommandMgr, RegisterCommandMgr, ReusableComponents, StartCommandMgr, WalletClaimCommandMgr
from src.managers.commands.BroadcastCommand import BroadcastCommandMgr
from src.managers.commands.OpenCommand import OpenCommandMgr


def initialize_dispatchers(dispatcher):
    # /signup command (register)
    add_registration_conversation(dispatcher)

    TIMEOUT_DURATION_IN_SECONDS = ReusableComponents.TIMEOUT_DURATION_IN_MINUTES * 60

    # /promocode command
    add_promo_code_conversation(dispatcher, TIMEOUT_DURATION_IN_SECONDS)
    # /exchange command
    add_exchange_conversation(dispatcher, TIMEOUT_DURATION_IN_SECONDS)
    # /wallet command
    add_wallet_conversation(dispatcher, TIMEOUT_DURATION_IN_SECONDS)
    # /quest command
    add_quest_conversation(dispatcher, TIMEOUT_DURATION_IN_SECONDS)
    # /mass command
    add_mass_broadcast_conversation(dispatcher)

    # /start command or when start button is pressed in telegram
    dispatcher.add_handler(CommandHandler("start", StartCommandMgr.start))
    # /open command
    dispatcher.add_handler(
        CommandHandler("open", OpenCommandMgr.surprise_box_start)
    )
    # /referralcode command
    dispatcher.add_handler(CommandHandler("referralcode", ReferralCodeCommandMgr.referral_code_instruction_start))

    # Log all errors
    dispatcher.add_error_handler(ReusableComponents.error)


def add_registration_conversation(dispatcher):
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler('signup', RegisterCommandMgr.new_user_reg_start)
            ],

            states=StateManager.get_registration_states(),

            fallbacks=StateManager.get_reg_fallback_handlers()
        )
    )


def add_promo_code_conversation(dispatcher, timeout_duration):
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler('promocode', PromoCommandMgr.promo_code_start)
            ],

            states=StateManager.get_promo_code_states(),

            fallbacks=StateManager.get_fallback_handler(),

            conversation_timeout=timeout_duration
        )
    )


def add_exchange_conversation(dispatcher, timeout_duration):
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler('exchange', ExchangeCommandMgr.exchange_start)
            ],

            states=StateManager.get_exchange_states(),

            fallbacks=StateManager.get_fallback_handler(),

            conversation_timeout=timeout_duration
        )
    )


def add_wallet_conversation(dispatcher, timeout_duration):
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler(
                    'wallet', WalletClaimCommandMgr.wallet_profile_start)
            ],

            states=StateManager.get_wallet_states(),

            fallbacks=StateManager.get_fallback_handler(),

            conversation_timeout=timeout_duration
        )
    )


def add_quest_conversation(dispatcher, timeout_duration):
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler(
                    'quests', QuestsCommandMgr.send_quest_image_start)
            ],

            states=StateManager.get_quest_states(),

            fallbacks=StateManager.get_fallback_handler(),

            conversation_timeout=timeout_duration
        )
    )


def add_mass_broadcast_conversation(dispatcher):
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler(
                    'mass', BroadcastCommandMgr.mass_broadcast_start)
            ],

            states=StateManager.get_mass_broadcast_states(),

            fallbacks=StateManager.get_fallback_handler()
        )
    )

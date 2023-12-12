from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.quote_response import QuoteResponse


T = TypeVar("T", bound="SwapRequest")


@_attrs_define
class SwapRequest:
    """
    Attributes:
        user_public_key (str): The user public key.
        quote_response (QuoteResponse):
        wrap_and_unwrap_sol (Union[Unset, bool]): Automatically wrap/unwrap SOL. If false, it will use wSOL token
            account.  Will be ignored if `destinationTokenAccount` is set because the `destinationTokenAccount` may belong
            to a different user that we have no authority to close. Default: True.
        use_shared_accounts (Union[Unset, bool]): This enables the usage of shared program accountns. That means no
            intermediate token accounts or open orders accounts need to be created for the users. But it also means that the
            likelihood of hot accounts is higher. Default: True.
        fee_account (Union[Unset, str]): Fee token account for the output token, it is derived using the seeds =
            ["referral_ata", referral_account, mint] and the `REFER4ZgmyYx9c6He5XfaTMiGfdLwRnkV4RPp9t9iF3` referral contract
            (only pass in if you set a `platformFeeBps` in `/quote` and make sure that the feeAccount has been created).
        prioritization_fee_lamports (Union[Unset, int]): The prioritization fee to pay in addition to the signature fee
            to prioritize the transaction.
        compute_unit_price_micro_lamports (Union[Unset, int]): The compute unit price to prioritize the transaction, the
            additional fee will be `computeUnitLimit * computeUnitPriceMicroLamports`. If `auto` is used, Jupiter will
            automatically set a priority fee and it will be capped at 5,000,000 lamports.
        as_legacy_transaction (Union[Unset, bool]): Request a legacy transaction rather than the default versioned
            transaction, needs to be paired with a quote using asLegacyTransaction otherwise the transaction might be too
            large.
        use_token_ledger (Union[Unset, bool]): This is useful when the instruction before the swap has a transfer that
            increases the input token amount. Then, the swap will just use the difference between the token ledger token
            amount and post token amount.
        destination_token_account (Union[Unset, str]): Public key of the token account that will be used to receive the
            token out of the swap. If not provided, the user's ATA will be used. If provided, we assume that the token
            account is already initialized.
        dynamic_compute_unit_limit (Union[Unset, bool]): Simulate the swap transaction to get the compute unit consumed,
            factor in a margin and set the ComputeBudget's compute unit limit.
    """

    user_public_key: str
    quote_response: "QuoteResponse"
    wrap_and_unwrap_sol: Union[Unset, bool] = True
    use_shared_accounts: Union[Unset, bool] = True
    fee_account: Union[Unset, str] = UNSET
    prioritization_fee_lamports: Union[Unset, int] = UNSET
    compute_unit_price_micro_lamports: Union[Unset, int] = UNSET
    as_legacy_transaction: Union[Unset, bool] = False
    use_token_ledger: Union[Unset, bool] = False
    destination_token_account: Union[Unset, str] = UNSET
    dynamic_compute_unit_limit: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_public_key = self.user_public_key
        quote_response = self.quote_response.to_dict()

        wrap_and_unwrap_sol = self.wrap_and_unwrap_sol
        use_shared_accounts = self.use_shared_accounts
        fee_account = self.fee_account
        prioritization_fee_lamports = self.prioritization_fee_lamports
        compute_unit_price_micro_lamports = self.compute_unit_price_micro_lamports
        as_legacy_transaction = self.as_legacy_transaction
        use_token_ledger = self.use_token_ledger
        destination_token_account = self.destination_token_account
        dynamic_compute_unit_limit = self.dynamic_compute_unit_limit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "userPublicKey": user_public_key,
                "quoteResponse": quote_response,
            }
        )
        if wrap_and_unwrap_sol is not UNSET:
            field_dict["wrapAndUnwrapSol"] = wrap_and_unwrap_sol
        if use_shared_accounts is not UNSET:
            field_dict["useSharedAccounts"] = use_shared_accounts
        if fee_account is not UNSET:
            field_dict["feeAccount"] = fee_account
        if prioritization_fee_lamports is not UNSET:
            field_dict["prioritizationFeeLamports"] = prioritization_fee_lamports
        if compute_unit_price_micro_lamports is not UNSET:
            field_dict["computeUnitPriceMicroLamports"] = compute_unit_price_micro_lamports
        if as_legacy_transaction is not UNSET:
            field_dict["asLegacyTransaction"] = as_legacy_transaction
        if use_token_ledger is not UNSET:
            field_dict["useTokenLedger"] = use_token_ledger
        if destination_token_account is not UNSET:
            field_dict["destinationTokenAccount"] = destination_token_account
        if dynamic_compute_unit_limit is not UNSET:
            field_dict["dynamicComputeUnitLimit"] = dynamic_compute_unit_limit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.quote_response import QuoteResponse

        d = src_dict.copy()
        user_public_key = d.pop("userPublicKey")

        quote_response = QuoteResponse.from_dict(d.pop("quoteResponse"))

        wrap_and_unwrap_sol = d.pop("wrapAndUnwrapSol", UNSET)

        use_shared_accounts = d.pop("useSharedAccounts", UNSET)

        fee_account = d.pop("feeAccount", UNSET)

        prioritization_fee_lamports = d.pop("prioritizationFeeLamports", UNSET)

        compute_unit_price_micro_lamports = d.pop("computeUnitPriceMicroLamports", UNSET)

        as_legacy_transaction = d.pop("asLegacyTransaction", UNSET)

        use_token_ledger = d.pop("useTokenLedger", UNSET)

        destination_token_account = d.pop("destinationTokenAccount", UNSET)

        dynamic_compute_unit_limit = d.pop("dynamicComputeUnitLimit", UNSET)

        swap_request = cls(
            user_public_key=user_public_key,
            quote_response=quote_response,
            wrap_and_unwrap_sol=wrap_and_unwrap_sol,
            use_shared_accounts=use_shared_accounts,
            fee_account=fee_account,
            prioritization_fee_lamports=prioritization_fee_lamports,
            compute_unit_price_micro_lamports=compute_unit_price_micro_lamports,
            as_legacy_transaction=as_legacy_transaction,
            use_token_ledger=use_token_ledger,
            destination_token_account=destination_token_account,
            dynamic_compute_unit_limit=dynamic_compute_unit_limit,
        )

        swap_request.additional_properties = d
        return swap_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.indexed_route_map_response import IndexedRouteMapResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    only_direct_routes: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    params["onlyDirectRoutes"] = only_direct_routes

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/indexed-route-map",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[IndexedRouteMapResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = IndexedRouteMapResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[IndexedRouteMapResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    only_direct_routes: Union[Unset, None, bool] = UNSET,
) -> Response[IndexedRouteMapResponse]:
    """GET /indexed-route-map

     Returns a hash map, input mint as key and an array of valid output mint as values, token mints are
    indexed to reduce the file size

    Args:
        only_direct_routes (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IndexedRouteMapResponse]
    """

    kwargs = _get_kwargs(
        only_direct_routes=only_direct_routes,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    only_direct_routes: Union[Unset, None, bool] = UNSET,
) -> Optional[IndexedRouteMapResponse]:
    """GET /indexed-route-map

     Returns a hash map, input mint as key and an array of valid output mint as values, token mints are
    indexed to reduce the file size

    Args:
        only_direct_routes (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IndexedRouteMapResponse
    """

    return sync_detailed(
        client=client,
        only_direct_routes=only_direct_routes,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    only_direct_routes: Union[Unset, None, bool] = UNSET,
) -> Response[IndexedRouteMapResponse]:
    """GET /indexed-route-map

     Returns a hash map, input mint as key and an array of valid output mint as values, token mints are
    indexed to reduce the file size

    Args:
        only_direct_routes (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IndexedRouteMapResponse]
    """

    kwargs = _get_kwargs(
        only_direct_routes=only_direct_routes,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    only_direct_routes: Union[Unset, None, bool] = UNSET,
) -> Optional[IndexedRouteMapResponse]:
    """GET /indexed-route-map

     Returns a hash map, input mint as key and an array of valid output mint as values, token mints are
    indexed to reduce the file size

    Args:
        only_direct_routes (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IndexedRouteMapResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            only_direct_routes=only_direct_routes,
        )
    ).parsed

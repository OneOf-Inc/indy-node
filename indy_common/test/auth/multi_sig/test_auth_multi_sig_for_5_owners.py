import pytest

from indy_common.authorize.auth_constraints import AuthConstraint, IDENTITY_OWNER


@pytest.fixture(scope='module')
def write_auth_req_validator(write_auth_req_validator, key):
    write_auth_req_validator.auth_cons_strategy.get_auth_constraint = lambda a: AuthConstraint(IDENTITY_OWNER, 5)
    return write_auth_req_validator


def test_claim_def_adding_success_5_owners(write_request_validation, req,
                                           identity_owners, key, write_auth_req_validator):
    req.signatures = {idr: "signature" for idr in identity_owners}
    assert write_request_validation(req, [key])


def test_claim_def_adding_fail_4_owners(write_request_validation, req,
                                        identity_owners, key):
    req.signatures = {idr: "signature" for idr in identity_owners[:4]}
    assert not write_request_validation(req, [key])


def test_claim_def_adding_fail_1_owner_4_unknown(write_request_validation, req,
                                                 identity_owners, key):
    req.signatures = {identity_owners[0]: "signature"}
    assert not write_request_validation(req, [key])

    owners_count = len(identity_owners)
    req.signatures.update({"unknown_idr_{}".format(i): "signature"
                           for i in range(owners_count, owners_count + 4)})
    assert not write_request_validation(req, [key])


def test_claim_def_adding_success_5_trustees(write_request_validation, req,
                                             trustees, key):
    req.signatures = {idr: "signature" for idr in trustees}
    assert not write_request_validation(req, [key])

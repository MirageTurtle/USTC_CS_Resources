package main

import (
	"fmt"
	"encoding/json"
	"strconv"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)


// SmartContract for managing accounts
type SmartContract struct {
	contractapi.Contract
}

// struct for an account
type Account struct {
	ID string `json:"id"`
	Name string `json:"name"`
	Balance string `json:"balance"`
}

// for handling result
type QueryResult struct {
	Key string `json:"key"`
	Record *Account
}

// init ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	accounts := []Account{
		Account{ID: "0000", Name: "Haoyuan Wang", Balance: "100"},
		Account{ID: "0001", Name: "Pingzhi Li", Balance: "100000"},
		Account{ID: "0002", Name: "Bo Peng", Balance: "20000"},
		Account{ID: "0003", Name: "Haotian Xu", Balance: "20000"},
	}
	for i, account := range accounts {
		accountAsBytes, _ := json.Marshal(account)
		err := ctx.GetStub().PutState("ACCOUNT" + strconv.Itoa(i), accountAsBytes)
		if err != nil {
			return fmt.Errorf("Failed to put to world state. %s", err.Error())
		}
	}
	return nil
}

func (s *SmartContract) CreateAccount(ctx contractapi.TransactionContextInterface, accountNumber string, id string, name string, balance string) error {
	account := Account{
		ID: id,
		Name: name,
		Balance: balance,
	}
	accountAsBytes, _ := json.Marshal(account)
	return ctx.GetStub().PutState(accountNumber, accountAsBytes)
}

func (s *SmartContract)QueryAccount(ctx contractapi.TransactionContextInterface, accountNumber string) (*Account, error) {
	accountAsBytes, err := ctx.GetStub().GetState(accountNumber)
	if err != nil {
		return nil, fmt.Errorf("Failed to read from world state. %s", err.Error())
	}
	if accountAsBytes == nil {
		return nil, fmt.Errorf("%s does not exist", accountNumber)
	}

	account := new(Account)
	_ = json.Unmarshal(accountAsBytes, account)
	return account, nil
}

func (s *SmartContract) QueryAllAccounts(ctx contractapi.TransactionContextInterface) ([]QueryResult, error) {
	startKey := ""
	endKey := ""
	resultsIterator, err := ctx.GetStub().GetStateByRange(startKey, endKey)
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	results := []QueryResult{}

	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}
		account := new(Account)
		_ = json.Unmarshal(queryResponse.Value, account)
		queryResult := QueryResult{Key: queryResponse.Key, Record: account}
		results = append(results, queryResult)
	}
	return results, nil
}

func (s *SmartContract) ChangeAccountBalance(ctx contractapi.TransactionContextInterface, accountNumber string, newBalance string) error {
	account, err := s.QueryAccount(ctx, accountNumber)
	if err != nil {
		return err
	}
	account.Balance = newBalance
	accountAsBytes, _ := json.Marshal(account)
	return ctx.GetStub().PutState(accountNumber, accountAsBytes)
}

func (s *SmartContract) DeleteAccount(ctx contractapi.TransactionContextInterface, accountNumber string) error {
	_, err := s.QueryAccount(ctx, accountNumber)
	if err != nil {
		return err
	}
	return ctx.GetStub().DelState(accountNumber)
}

func main() {
	chaincode, err := contractapi.NewChaincode(new(SmartContract))
	if err != nil {
		fmt.Printf("Error create fabric_bank chaincode: %s", err.Error())
		return
	}
	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting fabric_bank chaincode: %s", err.Error())
	}
}
// Fill out your copyright notice in the Description page of Project Settings.
#include "AvastYeCppBPFuncLibrary.h"

#include "EngineMinimal.h"
#include "UObjectIterator.h"


TArray<UClass*> UAvastYeCppBPFuncLibrary::GetClasses(UClass* ParentClass)
{
	TArray<UClass*> Results;

	// get our parent blueprint class
	const FString ParentClassName = ParentClass->GetName();
	UObject* ClassPackage = ANY_PACKAGE;
	UClass* ParentBPClass = FindObject<UClass>(ClassPackage, *ParentClassName);
	
	// iterate over UClass, this might be heavy on performance, so keep in mind..
	// better suggestions for a check are welcome
	for (TObjectIterator<UClass> It; It; ++It)
	{
		if (It->IsChildOf(ParentBPClass))
		{
			// It is a child of the Parent Class
			// make sure we don't include our parent class in the array (weak name check, suggestions welcome)
			if (It->GetName() != ParentClassName)
			{
				Results.Add(*It);
			}
		}
	}

	return Results;
}